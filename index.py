# https://pubmed.ncbi.nlm.nih.gov/?term=%22Cell%22%5BJournal%5D&sort=

from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
from public import *
from config import *

driver = webdriver.Chrome()
# https://pubmed.ncbi.nlm.nih.gov/?term=%22Cell%22%5BJournal%5D&sort=&page=2
# https://pubmed.ncbi.nlm.nih.gov/?term=%28%22Cell%22%5BJournal%5D%29+AND+%28%28%222020%22%5BDate+-+Publication%5D+%3A+%223000%22%5BDate+-+Publication%5D%29%29&sort=


driver.get("https://pubmed.ncbi.nlm.nih.gov/?term=%22Cell%22%5BJournal%5D&sort=&page=2")
articles = driver.find_elements_by_css_selector("article.full-docsum")
# print(articles)
articleList = []

for article in articles:
	# print(type(article))
	# print(article.text)
	texts = article.text.split("\n") #含有6个元素
	# print(len(texts))
	# print(texts)
	articleDic = {}
	articleDic["title"] = texts[2]
	articleDic["authors"] = texts[3].split(", ")
	articleDic["date"] = re.search(r"(\d\d\d\d ... \d+);",texts[4]).group(1)
	articleDic['date'].split(' ')
	articleDic['date'] = transformDate(day=articleDic['date'][2],month=articleDic['date'][1],year = articleDic['date'][0])
	articleDic["institution"] = re.search(r"^(.*?)\.",texts[4]).group(1)
	articleDic["pubmedUrl"] = article.find_elements_by_css_selector("a.docsum-title")[0].get_attribute("href")
	# print(articleDic)
	articleList.append(articleDic)

for article in articleList:
	driver.get(article["pubmedUrl"])
	abstract = driver.find_element_by_id("abstract").get_attribute("outerHTML")
	absoup = BeautifulSoup(abstract,"html.parser")
	ps = absoup.find_all("p")
	article["abstract"] = ps[0].get_text().strip()
	article['keywords'] = ps[1].get_text().replace("Keywords:","").strip().split('; ')
	urlsHTML = driver.find_element_by_id('linkout').get_attribute('outerHTML')
	ul = re.search(r"Full Text Sources.*?(<ul .*?>.*?</ul>)",urlsHTML,re.S).group(1)
	urlSoup = BeautifulSoup(ul,'html.parser')
	article['urlDic'] = urlSoup.find_all("li")
	article['urlDic'] = {item.get_text().strip():item.a['href'] for item in article['urlDic']}
	print(article)
	time.sleep(3)

# time.sleep(3)
driver.get("https://pubmed.ncbi.nlm.nih.gov/?term=%22Cell%22%5BJournal%5D&sort=&page=3")
time.sleep(3)
driver.close()
driver.quit()
