# -*- coding:utf-8 -*-

import os
from pymongo import MongoClient
import mod_config
import codecs


def create_TrainData():

    # 获得配置文件参数
    MongoDB_Host = mod_config.getConfig("database","db_AliYunSever_Host")
    MongoDB_Port = mod_config.getConfig("database","db_AliYunSever_Port")
    UniversityList = mod_config.get_University_list()

    #建立数据库连接
    conn = MongoClient(MongoDB_Host,int(MongoDB_Port))
    RawPOA = conn.RawPOA

    newsCollection = RawPOA["news"]

    for uni in UniversityList:

        path = './rawdata/' + uni["chn_name"] + "/"
        if not os.path.exists(path):
            os.makedirs(path)

        # 调取每个学校前50篇新闻作为训练数据集
        for iterm in newsCollection.find({"Uname": uni["chn_name"]}).limit(50):


            filePath = path + str(iterm["title"].encode("utf8")).strip() + ".txt"
            fileBody = iterm["body"]

            try:

                f = codecs.open(filePath,'w',"utf-8")
                f.write(fileBody)
                print filePath + "  写入成功"

            except Exception, e:
                print e
                print filePath + "  写入失败"

            finally:
                if f:
                    f.close()

# create_TrainData()

def copy_Data_from_Raw_to_Result():

    # 获得配置文件参数
    MongoDB_Host = mod_config.getConfig("database","db_AliYunSever_Host")
    MongoDB_Port = mod_config.getConfig("database","db_AliYunSever_Port")
    UniversityList = mod_config.get_University_list()

    #建立数据库连接
    conn = MongoClient(MongoDB_Host,int(MongoDB_Port))
    RawPOA = conn.RawPOA
    ResultPOA = conn.ResultPOA

    CopyList = []
    tempDict = {}

    for iterm in RawPOA["news"].find():

        tempDict = iterm
        tempDict["classification"] = "undefined"
        tempDict["sentiment"] = "99"
        CopyList.append(tempDict)
        print tempDict

    ResultPOA["news"].insert(CopyList)
    print "复制成功"

#copy_Data_from_Raw_to_Result()

def insert_university_list():
    # 获得配置文件参数
    MongoDB_Host = mod_config.getConfig("database","db_AliYunSever_Host")
    MongoDB_Port = mod_config.getConfig("database","db_AliYunSever_Port")
    UniversityList = mod_config.get_University_list()

    #建立数据库连接
    conn = MongoClient(MongoDB_Host,int(MongoDB_Port))
    ResultPOA = conn.ResultPOA

    ResultPOA["universitylist"].insert(UniversityList)
    print "插入成功"

#insert_university_list()


def create_NewsNumbersInfo():
    # 获得配置文件参数
    MongoDB_Host = mod_config.getConfig("database","db_AliYunSever_Host")
    MongoDB_Port = mod_config.getConfig("database","db_AliYunSever_Port")
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
    print "保存成功"

create_NewsNumbersInfo()





