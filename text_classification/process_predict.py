# -*- coding:utf-8 -*-
import mod_config

import jieba
from pymongo import MongoClient
import  cPickle as pickle
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.datasets import load_files


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

    # stopwordlist = readFile("./hlt_stop_words.txt").splitlines()
    # count_vect = CountVectorizer(stop_words=stopwordlist,max_df=0.5)
    # tfidf_transformer = TfidfTransformer()
    # train_data = load_files(typeDict["load_Files_Path"],categories=typeDict["categories"])
    # tfidf_transformer.fit_transform(count_vect.fit_transform(train_data.data))

    count_vect = readBunchObj(typeDict["count_vect_Path"])
    tfidf_transformer = readBunchObj(typeDict["tfidf_Path"])

    X_new_counts = count_vect.transform(docs)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)

    return X_new_tfidf


def get_predictedResult(tfidf,typeDict):

    clf = joblib.load(typeDict["save_model_Path"])
    result = clf.predict(tfidf)

    # 从numpy数组格式的结果提取出索引数值
    result_index = result[0]

    predictedResult = typeDict["categories"][result_index]

    return predictedResult


def main():

    # 获得配置文件参数
    MongoDB_Host = mod_config.getConfig("database","db_Host")
    MongoDB_Port = mod_config.getConfig("database","db_Port")
    UniversityList = mod_config.get_University_list()

    Dict = mod_config.get_ModelType_Info()

    #建立数据库连接
    conn = MongoClient(MongoDB_Host,int(MongoDB_Port))
    ResultPOA = conn.ResultPOA
    RawPOA = conn.RawPOA
    #LocalResultPOA = MongoClient('192.168.1.3',27017).ResultPOA

    # for uni in UniversityList:
    #
    #     InsertList = []
    #     for iterm in RawPOA["news"].find({"Uname": uni["zh_name"]}):
    #
    #         text_seg = seg_ChineseText(iterm["body"])
    #
    #         tfidf_sentiment = get_tfidf(text_seg,Dict["sentiment"])
    #         tfidf_classification = get_tfidf(text_seg,Dict["classification"])
    #
    #         sentimentResult = get_predictedResult(tfidf_sentiment,Dict["sentiment"])
    #         classificationResult = get_predictedResult(tfidf_classification,Dict["classification"])
    #
    #         newsDoc = iterm
    #         newsDoc["sentiment"] = sentimentResult
    #         newsDoc["classification"] = classificationResult
    #         InsertList.append(newsDoc)
    #
    #     ResultPOA["news"].insert(InsertList)
    #     #LocalResultPOA["news"].insert(InsertList)
    #     print uni["zh_name"] + "的新闻信息已保存完毕"

    str = "上海海事大学2017年拟录取硕士研究生名单公示"

    text_seg = seg_ChineseText(str)

    tfidf_sentiment = get_tfidf(text_seg, Dict["sentiment"])
    tfidf_classification = get_tfidf(text_seg, Dict["classification"])

    sentimentResult = get_predictedResult(tfidf_sentiment, Dict["sentiment"])
    classificationResult = get_predictedResult(tfidf_classification, Dict["classification"])

    print "待分类预测文本:'{0}' 的分类结果为:\n 情感分类:{1}\n 类别分类:{2}\n".format(str,sentimentResult,classificationResult)





    #print sentimentResult
    #print classificationResult


main()


