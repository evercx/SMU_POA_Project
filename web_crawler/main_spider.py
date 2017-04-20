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

#设置默认编码为utf-8
reload(sys)
sys.setdefaultencoding( "utf-8" )


# 请求新闻站点。输入为包含大学中英文名称的Dict。
def request_NewsInfo(university):

    # 请求地址模板
    base_url = "http://news.baidu.com/ns?word={school}&pn={number}&rn=20"

    # 设置用户代理
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}

    # 返回结果为该高校的新闻数组集合
    response_result = []

    #每个学校取200条左右的新闻数据
    for i in range(0,200,20):
        url=base_url.format(school=university["chn_name"],number=i)
        print "开始请求: " + url
        time.sleep(3)
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
                    print "正文处理完毕"
                    print parseHTMLResult["title"]
                    Uname = university["chn_name"]
                    abbr = university["en_name"]
                    document = {"Uname":Uname,"abbr":abbr,"title": parseHTMLResult["title"], "url": href, "date": date, "body":parseHTMLResult["body"]}
                    response_result.append(document)
                except Exception, e:
                    print e

        except urllib2.HTTPError,e:
            print e.reason

    return response_result;


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


    newsCollection = request_NewsInfo(UniversityList[0])
    save_DataToDB(newsCollection,RawPOA);

main()