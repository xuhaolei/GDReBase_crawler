# https://pubmed.ncbi.nlm.nih.gov/?term=%22Cell%22%5BJournal%5D&sort=

from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
from public import *
from config import *
from source import PubMedCentral
from source import ElsevierScience
from source import EuropePubMedCentral
from source import NaturePublishingGroup
from source import PublicLibraryofScience
from source import SilverchairInformationSystems
from source import Wiley
from source import HighWire

# 1 谷歌浏览器设置为无头模式
opts = webdriver.ChromeOptions()    # 声明一个谷歌配置对象
opts.set_headless() # 设置成无头
driver = webdriver.Chrome(chrome_options=opts)  # 选项注入

point = ''
with open('BreakPoint.txt','r',encoding='utf-8') as f:
	point = f.read().split(',')
point = [int(item) for item in point]
print(point)
fallsource = []
# https://pubmed.ncbi.nlm.nih.gov/?term=%22Cell%22%5BJournal%5D&sort=&page=2
# https://pubmed.ncbi.nlm.nih.gov/?term=%28%22Cell%22%5BJournal%5D%29+AND+%28%28%222020%22%5BDate+-+Publication%5D+%3A+%223000%22%5BDate+-+Publication%5D%29%29&sort=
journalCount = 0
i = 0
try:
	for journal in journals:
		journalCount += 1
		if journalCount < point[0]:
			continue
		for i in range(1,2000):
			if journalCount == point[0] and i < point[1]:
				continue
			print(journalCount,i)
			url = """https://pubmed.ncbi.nlm.nih.gov/?term=("%s"[Journal]) AND (("%s/%s/%s"[Date - Publication] : "%s/%s/%s"[Date - Publication]))&sort=pubdate&filter=simsearch1.fha&page=%d"""%('+'.join(journal[0].replace('&','').split(' ')),journal[1][0],journal[1][1],journal[1][2],journal[2][0],journal[2][1],journal[2][2],i)
			print(url)
			driver.get(url)
			# driver.get("https://pubmed.ncbi.nlm.nih.gov/?term=%22Cell%22%5BJournal%5D&sort=&page=2")
			articles = driver.find_elements_by_css_selector("article.full-docsum")
			if len(articles) == 0:
				break
			articleList = []
			for article in articles:
				try:

					texts = article.text.split("\n") #含有6个元素
					# print(len(texts))
					# print(texts)
					articleDic = {}
					articleDic["title"] = processTitle(texts[2])
					if db.havePaper(articleDic['title']):
						continue
					articleDic["authors"] = texts[3].split(", ")
					articleDic["date"] = re.search(r"(\d\d\d\d ... \d+)",texts[4]).group(1)
					articleDic['date'] = articleDic['date'].split(' ')
					articleDic['date'] = transformDate(day=articleDic['date'][2],month=articleDic['date'][1],year = articleDic['date'][0])
					articleDic["institution"] = re.search(r"^(.*?)\.",texts[4]).group(1)
					articleDic["pubmedUrl"] = article.find_elements_by_css_selector("a.docsum-title")[0].get_attribute("href")
					# print(articleDic)
					articleList.append(articleDic)
				except Exception as e:
					print(e)
					continue
			# print('2')
			for article in articleList:
				# print(article)
				try:
					driver.get(article["pubmedUrl"])
				except:
					print('Message: timeout: Timed out receiving message from renderer: 299.437')
					continue
				try:
					urlsHTML = driver.find_element_by_id('linkout').get_attribute('outerHTML')
					ul = re.search(r"Full Text Sources.*?(<ul .*?>.*?</ul>)",urlsHTML,re.S).group(1)
				except:
					print('找不到全文')
					continue
				urlSoup = BeautifulSoup(ul,'html.parser')
				article['urlDic'] = urlSoup.find_all("li")
				article['urlDic'] = {item.get_text().strip().replace(' ',''):item.a['href'] for item in article['urlDic']}
				abstract = ''
				try:
					abstract = driver.find_element_by_id("abstract").get_attribute("outerHTML")
				except:
					pass
				absoup = BeautifulSoup(abstract,"html.parser")
				ps = absoup.find_all("p")
				if len(ps) >= 2:
					article["abstract"] = processTitle(ps[0].get_text().strip())
					article['keywords'] = processTitle(ps[1].get_text().replace("Keywords:","").strip()).split('; ')
				elif len(ps) == 1:
					article["abstract"] = processTitle(ps[0].get_text().strip())
					article['keywords'] = []
				else:
					print('找不到摘要')
					article['abstract'] = ''
					article['keywords'] = []
				print(journal)
				print(url)
				if caculateScore(article['title']+article['abstract']) < 1: # 不是需要的文章
					article['valid'] = '0'
					article['contents'] = ''
					for k in article['urlDic']:
						article['url'] = article['urlDic'][k]
						break
					a = Article(article)
					print(article)
					a.toFile("files/%s.txt"%(article["title"][0:min(20,len(article["title"]))]),False)
					continue
				flag = False
				for item in prioritySources:
					if article['urlDic'].get(item) == None:
						continue
					flag = True
					article['url'] = article['urlDic'][item]
					article['valid'] = '1'
					# print(article['url'])
					print("%s.%s(url='%s',driver=driver).get_text()"%(str(item),str(item),str(article['url'])))
					# 此处直接转
					article['contents'] = eval("%s.%s(url='%s',driver=driver).get_text()"%(str(item),str(item),str(article['url'])))
					a = Article(article)
					print(article)
					a.toFile("files/%s.txt"%(article["title"][0:min(20,len(article["title"]))]),True)
					break
				if not flag:
					article['contents'] = ''
					for k in article['urlDic']:
						article['url'] = article['urlDic'][k]
						break
					article['valid'] = '1'
					a = Article(article)
					print(article)
					a.toFile("files/%s.txt"%(article["title"][0:min(20,len(article["title"]))]),False)
					fallsource.append(article['urlDic'])
				
				time.sleep(3)
except Exception as e:
	print('error0')
	print(e)
	raise Exception
	pass
finally:
	print(fallsource) #打印出失败的源
	bpoint = str(journalCount)+","+str(i)
	with open('BreakPoint.txt','w',encoding='utf-8') as f:
		f.write(bpoint)
	driver.close()
	driver.quit()

