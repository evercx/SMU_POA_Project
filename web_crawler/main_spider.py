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
                    Uname = university["chn_name"]
                    abbr = university["en_name"]
                    document = {"Uname":Uname,"abbr":abbr,"title": parseHTMLResult["title"], "url": href, "date": date, "body":parseHTMLResult["body"]}
                    if filter(document) == "true":
                        response_result.append(document)
                except Exception, e:
                    print e

        except urllib2.HTTPError,e:
            print e.reason

    return response_result


# 过滤一些无效的新闻数据
def filter(doc):

    if doc["body"] == "error":
        return "false"

    if len(doc["body"]) <= 50:
        return "false"

    return "true"


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

    for uni in UniversityList:
        count += 1
        print "开始爬取第"+str(count)+"个学校数据,还有"+str(len(UniversityList)-count)+"个学校爬取"

        newsCollection = request_NewsInfo(uni)
        save_DataToDB(newsCollection, RawPOA)
        print uni["chn_name"] + "的新闻爬取完毕。共"+str(len(newsCollection))+"条信息数据\n"

    print "所有学校数据爬取完毕"



def s():
    # 获得配置文件参数
    MongoDB_Host = mod_config.getConfig("database","db_AliYunSever_Host")
    MongoDB_Port = mod_config.getConfig("database","db_AliYunSever_Port")
    UniversityList = mod_config.get_University_list()

    #建立数据库连接
    conn = MongoClient(MongoDB_Host,int(MongoDB_Port))
    RawPOA = conn.RawPOA

    #计数器
    count = 0

    for i in range(17,20):
        count += 1
        print "开始爬取第" + str(count) + "个学校数据,还有" + str(3 - count) + "个学校爬取"

        newsCollection = request_NewsInfo(UniversityList[i])
        save_DataToDB(newsCollection, RawPOA)
        print UniversityList[i]["chn_name"] + "的新闻爬取完毕。共" + str(len(newsCollection)) + "条信息数据\n"

    print "所有学校数据爬取完毕"

#main()

s()