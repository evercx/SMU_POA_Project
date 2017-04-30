# -*- coding:utf-8 -*-

import urllib2
import sys
import re
from readability import Document
import html2text
import time
import mod_config
from pymongo import MongoClient
from bs4 import BeautifulSoup
import time

reload(sys)
sys.setdefaultencoding('utf8')


# 请求新闻站点。输入为包含大学中英文名称的Dict。
def request_NewsInfo(university):

    # 请求地址模板
    base_url = "http://news.baidu.com/ns?word={school}&pn={number}&rn=20&cl=2"

    # 设置用户代理
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    headers = {'User-Agent': user_agent}

    #repeat = False

    # 返回结果为该高校的新闻数组集合
    response_result = []
    
    tempConstractList = []

    #每个学校取200条左右的新闻数据
    for i in range(0,740,20):
        tempList = []
        url=base_url.format(school=university["zh_name"],number=i)
        print "Request begin:" + base_url.format(school=university["en_name"],number=i)
        time.sleep(2)
        
        try:
            request=urllib2.Request(url,headers=headers)
            html=urllib2.urlopen(request).read()
            re_result=r'<h3 class="c-title">(.*?)<span class="c-info">'
            re_href=r'<a href="(.*?)"'
            re_date=r'<p class="c-author">.*?&nbsp;&nbsp;(.*?)</p>'
            result=re.findall(re_result,html,re.S|re.M)

            for detail in result:
                href=re.findall(re_href,detail,re.S|re.M)[0]
                try:
                    date=re.findall(re_date,detail,re.S|re.M)[0]
                except Exception,e:
                    date = "暂无日期"
                    print e

                time.sleep(1)
                try:
                    html = urllib2.urlopen(href, timeout=5).read()
                    parseHTMLResult = process_BodyText(html)
                    Uname = university["zh_name"]
                    abbr = university["en_name"]
                    document = {"Uname":Uname,"abbr":abbr,"title": parseHTMLResult["title"], "url": href, "date": date, "body":parseHTMLResult["body"]}
                    if filter(document,response_result) == "true":
                        tempList.append(document)
                    # if filter(document,response_result) == "repeat":
                    #     repeat = True
                       
                except Exception, e:
                    print e

        except urllib2.HTTPError,e:
            print e.reason

        if (tempConstractList == tempList):
            tempConstractList = []
            break;
        tempConstractList = tempList
        for o in tempList:
            response_result.append(o)
        print "The System has Downloaded " + str(len(response_result)) +" news of " + university["en_name"];

    return response_result


# 过滤一些无效的新闻数据
def filter(doc,List):

    if doc["body"] == "error":
        return "false"

    if len(doc["body"]) <= 50:
        return "false"

    if len(doc["date"]) <= 10:
        return "false"

    if doc["body"].find('ä') != -1:
        return "false"

    if doc["title"].find('ä') != -1:
        return "false"
    
    # if(findInList(List,"title",doc["title"]) != -1):
    #     return "repeat"

    if(findInList(List,"url",doc["url"]) != -1):
        return "repeat"
    

    return "true"


def findInList(List,key,value):
    count = 0
    #print List
    #print key
    #print value +'\n'
    for element in List:
        if(element[key] == value):
            return count
        count = count + 1
    return -1


# 处理不同来源新闻页面的HTML正文函数。 输入参数:页面HTML代码。
def process_BodyText(html):
    try:

        soup = BeautifulSoup(html, "lxml")
        readable_article = Document(html).summary()
        result = html2text.html2text(readable_article)
        returnResult = {"title":soup.title.string,"body":result}
        return returnResult

    except Exception,e:
        print e
        return {"title":"error","body":"error"}


# 保存数据函数。输入参数:插入数据,数据库名称实例
def save_DataToDB(documents,DBName):
    DBName["news"].insert(documents)



def main():

    # 获得配置文件参数
    MongoDB_Host = mod_config.getConfig("database","db_AliYunSever_Host")
    MongoDB_Port = mod_config.getConfig("database","db_AliYunSever_Port")
    UniversityList = mod_config.get_University_list()

    #建立数据库连接
    conn = MongoClient(MongoDB_Host,int(MongoDB_Port))
    RawPOA = conn.RawPOA

    #计数器
    count = 0

    ISOTIMEFORMAT='%Y-%m-%d %X'

    print time.strftime( ISOTIMEFORMAT, time.localtime() )
    #print "/n"

    for uni in UniversityList:
        count += 1
        #print "开始爬取第"+str(count)+"个学校数据,还有"+str(len(UniversityList)-count)+"个学校爬取"
        print "The system begins to download the "+str(count)+"st university. There are "+str(len(UniversityList)-count)+" universities left."

        newsCollection = request_NewsInfo(uni)
        save_DataToDB(newsCollection, RawPOA)
        #print  + "的新闻爬取完毕。共"+str(len(newsCollection))+"条信息数据\n"
        print "The system has finished downloading the news of "+uni["en_name"]+". There are total "+str(len(newsCollection))+" news.\n"

        print time.strftime( ISOTIMEFORMAT, time.localtime() )
        #print "/n"

    print "Work finished!\n"
    print time.strftime( ISOTIMEFORMAT, time.localtime() )
    #print "/n"


main()