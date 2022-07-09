SQLHOST="localhost"  #数据库地址
SQLPORT=3306         #数据库端口号
SQLUSER="root"       #用户名
SQLPASS="43420"      #数据库密码
SQLDB="bacterium_disease"       #所使用的数据库名称

import http.client
import hashlib
import json
import urllib
import random
import time


def baidu_translate(content):
    appid = '20200316000399558'
    secretKey = 'BK6HRAv6QJDGBwaZgr4F'
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = content
    fromLang = 'auto' # 源语言
    toLang = 'zh'   # 翻译后的语言
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
 
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        jsonResponse = response.read().decode("utf-8")# 获得返回的结果，结果为json格式
        js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构
        print(js)
        dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
        print(dst) # 打印结果
        return dst
    except Exception as e:
        print('err:'+e)
    finally:
        if httpClient:
            httpClient.close()

import requests
import MySQLdb
from bs4 import BeautifulSoup
import re
import time
from config import *
# from config import words

class Database:
    def __init__(self):
        # 打开数据库连接
        self.connection=MySQLdb.Connect(host=SQLHOST,user=SQLUSER,passwd=SQLPASS,db=SQLDB,port=SQLPORT, charset="utf8") #其中db是数据库的名字，，3306是一般数据库的地址
        # self.connection.close()
    def base(self,sql,get=False):                #相当于是基类
        try:
            # self.connection=MySQLdb.Connect(host=SQLHOST,user=SQLUSER,passwd=SQLPASS,db=SQLDB,port=SQLPORT, charset="utf8")
            with self.connection.cursor() as cursor:
                count = cursor.execute(sql)      # 影响的行数
                self.connection.commit()         # 提交事务
                if get:
                    result = cursor.fetchall()   # 取出所有行
                    return result
        except Exception as e:
            print("出错了")
            print(e)
            self.connection.rollback()           # 若出错了，则回滚
            raise Exception
        # finally:
        #     self.connection.close()
    def __del__(self):                           #当程序结束时运行
        self.connection.close()
    def addPaper(self,title,authors,date,institution,keywords,abstract,url,filename,valid):
        authorsStr = ""
        first = True
        for author in authors:
            if not first:
                authorsStr += ", "
            authorsStr += author
            first = False
        keywordsStr = ""
        first = True
        for keyword in keywords:
            if not first:
                keywordsStr += ", "
            keywordsStr += keyword
            first = False
        # print(url)
        title1 = re.sub('[^A-Za-z0-9]+', '', title)
        try:
            sql = r"""insert into `tb_paper`(`title`,`authors`,`date`,`institution`,`keywords`,`abstract`,`url`,`filename`,`valid`) values
                ("%s","%s","%s","%s","%s","%s","%s","%s",%s)"""%(title,authorsStr,date,institution,keywordsStr,abstract,url,filename,valid)
            # print(sql)
            self.base(sql)
        except:
            try:

                sql = r"""insert into `tb_paper`(`title`,`authors`,`date`,`institution`,`keywords`,`abstract`,`url`,`filename`,`valid`) values
                   ("%s","%s","%s","%s","%s","%s","%s","%s",%s)"""%(title1,authorsStr,date,institution,keywordsStr,abstract,url,filename,valid)
                # print(sql)
                self.base(sql)
            except:
                pass

    def havePaper(self,title):
        sql = r"""select * from `tb_paper` where `title`="%s" """%(title)
        res = self.base(sql,get=True)
        if res == None or len(res)==0:
            return False
        else:
            return True 

db = Database()

class Article(object):
    """docstring for Article"""
    def __init__(self, arg):
        super(Article, self).__init__()
        self.title = arg.get("title")# you
        self.authors = arg.get("authors")# you
        self.date = arg.get("date")# you
        self.institution = arg.get("institution")# you
        self.keywords = arg.get("keywords")
        self.abstract = arg.get('abstract')
        self.url = arg.get("url")# 
        self.contents = arg.get("contents")
        self.valid = arg.get("valid") # str

    def toFile(self,filename,wenable):
        db.addPaper(self.title,self.authors,self.date,self.institution,self.keywords,self.abstract,self.url,filename.split("/")[-1],self.valid)
        if wenable:
            with open(filename,"w",encoding="utf-8") as f:
                f.write(self.contents)

def transformDate(day,month,year):
    dic = {"January":"01","February":"02","March":"03","April":"04","May":"05","June":"06","July":"07","August":"08","September":"09","October":"10","November":"11","December":"12"}
    dic2 = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    keys = list(dic.keys())
    for key in keys:
        dic[key.lower()] = dic[key]
    keys = list(dic2.keys())
    for key in keys:
        dic2[key.lower()] = dic2[key]
    
    month1 = dic.get(month.lower())
    if month1 == None:
        month1 = dic2.get(month.lower())
    if month1 == None:
        month1 = "01" # 如果两个字典都找不到就是none
    return year+"-"+month1+"-"+day

def processTitle(title):
    return title.strip().replace("\n","").replace("\\","").replace("<","").replace(">","").replace('"','').replace('/','').replace('?','').replace('|','').replace(':','').replace('*','')

def caculateScore(title):
    title = title.lower()
    bdic = vaildWords[0]
    ddic = vaildWords[1]
    score = 0
    bscore = 0
    dscore = 0
    for key in bdic:
        s = bdic[key]
        keys = key.split('/')
        for k in keys:
            if k in title:
                bscore += s
                break
    for key in ddic:
        s = ddic[key]
        keys = key.split('/')
        for k in keys:
            if k in title:
                dscore += s
                break
    score = bscore + dscore
    return score

