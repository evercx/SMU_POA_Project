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

create_TrainData()