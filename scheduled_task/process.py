# -*- coding:utf-8 -*-
import mod_config
import os
import urllib2
import re
import sys
from readability import Document
from bs4 import BeautifulSoup
import html2text
import jieba
from pymongo import MongoClient
import pymongo as pym
import  cPickle as pickle
from sklearn.externals import joblib
import time


reload(sys)
sys.setdefaultencoding('utf8')

def readFile(path):

    f = open(path,"r")
    content = f.read()
    f.close()
    return content


def readBunchObj(path):

    file_Obj = open(path,"rb")
    bunch = pickle.load(file_Obj)
    file_Obj.close()
    return bunch

def seg_ChineseText(text):

    str = text.strip().replace("\r\n","").strip()
    text_seg = " ".join(jieba.cut(str))

    return text_seg


def get_tfidf(text_seg,typeDict):

    docs = []
    docs.append(text_seg)

    count_vect = readBunchObj(typeDict["count_vect_Path"])
    tfidf_transformer = readBunchObj(typeDict["tfidf_Path"])

    X_new_counts = count_vect.transform(docs)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)

    return X_new_tfidf


def get_predictedResult(tfidf,typeDict):

    clf = joblib.load(typeDict["save_model_Path"])
    result = clf.predict(tfidf)

    predictedResult = typeDict["categories"][result]

    return predictedResult


def get_ModelType_Info():

    return {

        "sentiment":{
            "categories": ["-1", "0", "1"],
            "load_Files_Path": './sentiment_seg_data/',
            "save_model_Path": os.getcwd() +'/models/sentiment_model.m',
            "count_vect_Path": os.getcwd() +'/wordbag/sentiment_count_vect.dat',
            "tfidf_Path": os.getcwd() +'/wordbag/sentiment_tfidf.dat'
        },

        "classification":{
            "categories": ["activity", "entrance", "social","study"],
            "load_Files_Path": './classification_seg_data/',
            "save_model_Path": os.getcwd() +'/models/classification_model.m',
            "count_vect_Path": os.getcwd() +'/wordbag/classification_count_vect.dat',
            "tfidf_Path": os.getcwd() +'/wordbag/classification_tfidf.dat'
        },
    }

def main():

    Dict = get_ModelType_Info()

    str = "2017上海海事大学研究生入学考试简章"
    text_seg = seg_ChineseText(str);



    tfidf_sentiment = get_tfidf(text_seg, Dict["sentiment"])
    tfidf_classification = get_tfidf(text_seg, Dict["classification"])

    sentimentResult = get_predictedResult(tfidf_sentiment, Dict["sentiment"])
    classificationResult = get_predictedResult(tfidf_classification, Dict["classification"])

    Result = {
        "sentiment":sentimentResult,
        "classification":classificationResult,
        # "text":sys.argv[1]
    }

    print Result

#main()


# def demo():
#     # 获得配置文件参数
#     MongoDB_Host = mod_config.getConfig("database","db_Host")
#     MongoDB_Port = mod_config.getConfig("database","db_Port")
#     UniversityList = mod_config.get_University_list()
#
#     #建立数据库连接
#     conn = MongoClient(MongoDB_Host,int(MongoDB_Port))
#     ResultPOA = conn.ResultPOA
#     #ResultList = []
#
#     ResultPOA["tempNews"].drop()
#     for uni in UniversityList:
#         ResultList = []
#         for iterm in ResultPOA["news"].find({"Uname": uni["zh_name"]}).sort("date",pym.DESCENDING).limit(20):
#             if iterm["date"].encode("utf-8") != "暂无日期":
#                 doc = {
#                     "body":iterm["body"],
#                     "title":iterm["title"],
#                     "url":iterm["url"],
#                     "Uname":iterm["Uname"],
#                     "abbr":iterm["abbr"],
#                     "date":iterm["date"],
#                     "sentiment":iterm["sentiment"],
#                     "classification":iterm["classification"]
#                 }
#                 ResultList.append(doc)
#
#         ResultPOA["tempNews"].insert(ResultList)
#         print "success"
#
# demo()



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


# 过滤一些无效的新闻数据
def filter(doc):
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

    return "true"

def spider():

    UniversityList = mod_config.get_University_list()
    resultList = {}

    #初始化新闻集合的数据结构
    for uni in UniversityList:
        resultList[uni["zh_name"]] = []

    # 请求地址模板
    base_url = "http://news.baidu.com/ns?word={school}&pn=0&rn=20&cl=2"

    # 设置用户代理
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    headers = {'User-Agent': user_agent}

    #开始爬取20个学校的最近新闻
    for uni in UniversityList:
        url = base_url.format(school=uni["zh_name"])
        print "开始爬取" + uni["zh_name"] +"..."
        time.sleep(2)

        try:
            request = urllib2.Request(url, headers=headers)
            html = urllib2.urlopen(request).read()
            re_result = r'<h3 class="c-title">(.*?)<span class="c-info">'
            re_href = r'<a href="(.*?)"'
            re_date = r'<p class="c-author">.*?&nbsp;&nbsp;(.*?)</p>'
            result = re.findall(re_result, html, re.S | re.M)

            for detail in result:
                href = re.findall(re_href, detail, re.S | re.M)[0]
                try:
                    date = re.findall(re_date, detail, re.S | re.M)[0]
                except Exception, e:
                    date = "暂无日期"
                    print e

                time.sleep(1)
                try:
                    request = urllib2.Request(href, headers=headers)
                    html = urllib2.urlopen(request,timeout=5).read()
                    parseHTMLResult = process_BodyText(html)
                    Uname = uni["zh_name"]
                    abbr = uni["en_name"]
                    document = {"Uname": Uname, "abbr": abbr, "title": parseHTMLResult["title"], "url": href,
                                "date": date, "body": parseHTMLResult["body"]}
                    if filter(document) == "true":
                        resultList[uni["zh_name"]].append(document)
                except Exception, e:
                    print e
        except urllib2.HTTPError, e:
            print e.reason

    print "爬虫完毕\n"
    return resultList






def findUrlInList(url,list):

    index = 0
    for i in list:
        if url == i["url"]:
            return index
        index = index + 1

    return -1




def predict(str):

    Dict = get_ModelType_Info()

    #str = "2017上海海事大学研究生入学考试简章"
    text_seg = seg_ChineseText(str);


    tfidf_sentiment = get_tfidf(text_seg, Dict["sentiment"])
    tfidf_classification = get_tfidf(text_seg, Dict["classification"])

    sentimentResult = get_predictedResult(tfidf_sentiment, Dict["sentiment"])
    classificationResult = get_predictedResult(tfidf_classification, Dict["classification"])

    Result = {
        "sentiment":sentimentResult,
        "classification":classificationResult,
    }

    return Result


def update_NewsNumbersInfo():
    # 获得配置文件参数
    MongoDB_Host = mod_config.getConfig("database","db_Host")
    MongoDB_Port = mod_config.getConfig("database","db_Port")
    UniversityList = mod_config.get_University_list()

    #建立数据库连接
    conn = MongoClient(MongoDB_Host,int(MongoDB_Port))
    ResultPOA = conn.ResultPOA
    ResultList = []

    for uni in UniversityList:

        studyNumberList = []
        activityNumberList = []
        entranceNumberList = []
        socialNumberList = []

        studyNumberList.append(ResultPOA["news"].find({"Uname": uni["zh_name"], "classification": "study", "sentiment": "-1"}).count())
        studyNumberList.append(ResultPOA["news"].find({"Uname": uni["zh_name"], "classification": "study", "sentiment": "0"}).count())
        studyNumberList.append(ResultPOA["news"].find({"Uname": uni["zh_name"], "classification": "study", "sentiment": "1"}).count())
        studyNumberList.append(studyNumberList[0] + studyNumberList[1] + studyNumberList[2])

        activityNumberList.append(ResultPOA["news"].find({"Uname": uni["zh_name"], "classification": "activity", "sentiment": "-1"}).count())
        activityNumberList.append(ResultPOA["news"].find({"Uname": uni["zh_name"], "classification": "activity", "sentiment": "0"}).count())
        activityNumberList.append(ResultPOA["news"].find({"Uname": uni["zh_name"], "classification": "activity", "sentiment": "1"}).count())
        activityNumberList.append(activityNumberList[0] + activityNumberList[1] + activityNumberList[2])


        entranceNumberList.append(ResultPOA["news"].find({"Uname": uni["zh_name"], "classification": "entrance", "sentiment": "-1"}).count())
        entranceNumberList.append(ResultPOA["news"].find({"Uname": uni["zh_name"], "classification": "entrance", "sentiment": "0"}).count())
        entranceNumberList.append(ResultPOA["news"].find({"Uname": uni["zh_name"], "classification": "entrance", "sentiment": "1"}).count())
        entranceNumberList.append(entranceNumberList[0] + entranceNumberList[1] + entranceNumberList[2])

        socialNumberList.append(ResultPOA["news"].find({"Uname": uni["zh_name"], "classification": "social", "sentiment": "-1"}).count())
        socialNumberList.append(ResultPOA["news"].find({"Uname": uni["zh_name"], "classification": "social", "sentiment": "0"}).count())
        socialNumberList.append(ResultPOA["news"].find({"Uname": uni["zh_name"], "classification": "social", "sentiment": "1"}).count())
        socialNumberList.append(socialNumberList[0] + socialNumberList[1] + socialNumberList[2])


        # print uni["zh_name"]
        # print studyNumberList
        # print activityNumberList
        # print entranceNumberList
        # print socialNumberList

        ResultList.append({"Uname":uni["zh_name"],"abbr":uni["en_name"],"studyNumber":studyNumberList,"activityNumber":activityNumberList,"entranceNumber":entranceNumberList,"socialNumber":socialNumberList})

    ResultPOA["newsNumber"].drop()
    ResultPOA["newsNumber"].insert(ResultList)
    print "新闻数目更新成功\n"



def mainTask():

    # 获得配置文件参数
    MongoDB_Host = mod_config.getConfig("database","db_Host")
    MongoDB_Port = mod_config.getConfig("database","db_Port")
    UniversityList = mod_config.get_University_list()

    #建立数据库连接
    conn = MongoClient(MongoDB_Host,int(MongoDB_Port))
    RawPOA = conn.RawPOA
    ResultPOA = conn.ResultPOA


    raw_tempList = {}
    result_tempList = {}

    for uni in UniversityList:
        raw_tempList[uni["zh_name"]] = []
        result_tempList[uni["zh_name"]] = []

    print "从缓存新闻表中取出数据..."
    for uni in UniversityList:
        for iterm in RawPOA["tempNews"].find({"Uname": uni["zh_name"]}).sort("date",pym.DESCENDING).limit(20):
            if iterm["date"].encode("utf-8") != "暂无日期":
                doc = {
                    "body":iterm["body"],
                    "title":iterm["title"],
                    "url":iterm["url"],
                    "Uname":iterm["Uname"],
                    "abbr":iterm["abbr"],
                    "date":iterm["date"]
                }
                raw_tempList[uni["zh_name"]].insert(0,doc)

        for iterm in ResultPOA["tempNews"].find({"Uname": uni["zh_name"]}).sort("date",pym.DESCENDING).limit(20):
            if iterm["date"].encode("utf-8") != "暂无日期":
                doc = {
                    "body":iterm["body"],
                    "title":iterm["title"],
                    "url":iterm["url"],
                    "Uname":iterm["Uname"],
                    "abbr":iterm["abbr"],
                    "date":iterm["date"],
                    "sentiment":iterm["sentiment"],
                    "classification":iterm["classification"]
                }
                result_tempList[uni["zh_name"]].insert(0,doc)

    print "从缓存新闻表中取出数据成功\n\n"

    spiderList = spider()

    print "开始查重去重操作..."

    for uni in UniversityList:
        count = 0
        predictedList = []
        for iterm in spiderList[uni["zh_name"]]:
            if (findUrlInList(iterm["url"],raw_tempList[uni["zh_name"]]) == -1) and (findUrlInList(iterm["url"],result_tempList[uni["zh_name"]])):
                count = count + 1
                raw_tempList[uni["zh_name"]].insert(0,iterm)
                predictResult = predict(iterm["body"])
                tempIterm = {
                    "body": iterm["body"],
                    "title": iterm["title"],
                    "url": iterm["url"],
                    "Uname": iterm["Uname"],
                    "abbr": iterm["abbr"],
                    "date": iterm["date"],
                    "sentiment":predictResult["sentiment"],
                    "classification":predictResult["classification"]

                }
                result_tempList[uni["zh_name"]].insert(0, tempIterm)
                predictedList.append(tempIterm)

        for i in range(0,count):
            raw_tempList[uni["zh_name"]].pop()
            result_tempList[uni["zh_name"]].pop()

        ResultPOA["news"].insert(predictedList)
        print "结果数据表的数据保存成功"

    print "去重操作完成\n\n"

    RawPOA["tempNews"].drop()
    ResultPOA["tempNews"].drop()
    for uni in UniversityList:
        RawPOA["tempNews"].insert(raw_tempList[uni["zh_name"]])
        ResultPOA["tempNews"].insert(result_tempList[uni["zh_name"]])

    print "数据库存入数据成功\n\n"

    update_NewsNumbersInfo()


mainTask()


