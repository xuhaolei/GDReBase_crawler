# # from source import PubMedCentral
# # from selenium import webdriver
# # help(PubMedCentral)
# # driver = webdriver.Chrome()
# # try:
# # 	print(PubMedCentral.PubMedCentral("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7428724/",driver).get_text())
# # except Exception as e:
# # 	print(e)
# # finally:
# # 	driver.close()
# # 	driver.quit()
# SQLHOST="localhost"  #数据库地址
# SQLPORT=3306         #数据库端口号
# SQLUSER="root"       #用户名
# SQLPASS="43420"      #数据库密码
# SQLDB="bacterium_disease"       #所使用的数据库名称

# import http.client
# import hashlib
# import json
# import urllib
# import random
# import time


# def baidu_translate(content):
#     appid = '20200316000399558'
#     secretKey = 'BK6HRAv6QJDGBwaZgr4F'
#     httpClient = None
#     myurl = '/api/trans/vip/translate'
#     q = content
#     fromLang = 'auto' # 源语言
#     toLang = 'zh'   # 翻译后的语言
#     salt = random.randint(32768, 65536)
#     sign = appid + q + str(salt) + secretKey
#     sign = hashlib.md5(sign.encode()).hexdigest()
#     myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
#         q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
#         salt) + '&sign=' + sign
 
#     try:
#         httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
#         httpClient.request('GET', myurl)
#         # response是HTTPResponse对象
#         response = httpClient.getresponse()
#         jsonResponse = response.read().decode("utf-8")# 获得返回的结果，结果为json格式
#         js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构
#         # print(js)
#         dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
#         # print(dst) # 打印结果
#         return dst
#     except Exception as e:
#         print('err:'+e)
#     finally:
#         if httpClient:
#             httpClient.close()
# import requests
# import MySQLdb
# from bs4 import BeautifulSoup
# import re
# import time
# from config import *
# # from config import words

# class Database:
#     def __init__(self):
#         # 打开数据库连接
#         self.connection=MySQLdb.Connect(host=SQLHOST,user=SQLUSER,passwd=SQLPASS,db=SQLDB,port=SQLPORT, charset="utf8") #其中db是数据库的名字，，3306是一般数据库的地址
#         # self.connection.close()
#     def base(self,sql,get=False):                #相当于是基类
#         try:
#             # self.connection=MySQLdb.Connect(host=SQLHOST,user=SQLUSER,passwd=SQLPASS,db=SQLDB,port=SQLPORT, charset="utf8")
#             with self.connection.cursor() as cursor:
#                 count = cursor.execute(sql)      # 影响的行数
#                 self.connection.commit()         # 提交事务
#                 if get:
#                     result = cursor.fetchall()   # 取出所有行
#                     return result
#         except Exception as e:
#             print("出错了")
#             print(e)
#             self.connection.rollback()           # 若出错了，则回滚
#             raise Exception
#         # finally:
#         #     self.connection.close()
#     def __del__(self):                           #当程序结束时运行
#         self.connection.close()
#     def addPaper(self,title,authors,date,institution,keywords,abstract,url,filename,valid):
#         authorsStr = ""
#         first = True
#         for author in authors:
#             if not first:
#                 authorsStr += ", "
#             authorsStr += author
#             first = False
#         keywordsStr = ""
#         first = True
#         for keyword in keywords:
#             if not first:
#                 keywordsStr += ", "
#             keywordsStr += keyword
#             first = False
#         # print(url)

#         sql = r"""insert into `paper`(`title`,`authors`,`date`,`institution`,`keywords`,`abstract`,`url`,`filename`,`valid`) values
#                 ("%s","%s","%s","%s","%s","%s","%s","%s",%s)"""%(title,authorsStr,date,institution,keywordsStr,abstract,url,filename,valid)
#         # print(sql)
#         self.base(sql)
#     def havePaper(self,title):
#         sql = r"""select * from `paper` where `title`="%s" """%(title)
#         res = self.base(sql,get=True)
#         if res == None or len(res)==0:
#             return False
#         else:
#             return True 
#     def selectPaper(self,pid):
#     	sql = r"""select * from `paper` where `id`=%s"""%pid
#     	res = self.base(sql,get=True)
#     	if res == None or len(res)==0:
#     		return []
#     	else:
#     		return res
# # 12332
# db = Database()
# # print(db.selectPaper('155'))
# excel = {"pid":[],"real":[],"result":[],"get":[]}
# import random
# count = 0
# for i in range(130):
# 	pid = str(random.randint(155,155+12332))
# 	if pid in excel['pid']:
# 		continue
# 	res = db.selectPaper(pid)
# 	if len(res) == 0:
# 		continue
# 	t = baidu_translate(res[0][1])
# 	time.sleep(1)
# 	count += 1
# 	print("标题：",t)
# 	t = baidu_translate(str(res[0][6]))
# 	print("摘要：",t)
# 	r = input("请输入0:不是，1:是")
# 	while r!='0' and r!='1':
# 		r = input("输入有误，请再次输入(0或1)：")
# 	excel['pid'].append(pid)
# 	excel['real'].append(int(r))
# 	excel['result'].append(int(res[0][-1]>0))
# 	excel['get'].append(int(res[0][-1]==1))
# 	if count >= 100:
# 		break

# print(excel)
# import pandas as pd
# # pd.DataFrame(excel)
# save = pd.DataFrame(excel)
# save.to_csv('test.csv',index=False)
journal = ('NATURE REVIEWS DRUG DISCOVERY', ('2021', '05', '01'), ('2021', '10', '01'))
i = 1
url = """https://pubmed.ncbi.nlm.nih.gov/?term=("%s"[Journal) AND (("%s/%s/%s"[Date - Publication] : "%s/%s/%s"[Date - Publication]))&sort=pubdate&filter=simsearch1.fha&page=%d"""%('+'.join(journal[0].replace('&','').split(' ')),journal[1][0],journal[1][1],journal[1][2],journal[2][0],journal[2][1],journal[2][2],i)
print(url)


