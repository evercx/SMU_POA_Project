# -*- coding:utf-8 -*-
import mod_config

import jieba
from pymongo import MongoClient
import  cPickle as pickle
from sklearn.externals import joblib

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


def main():
    Dict = mod_config.get_ModelType_Info()
    text_seg = seg_ChineseText("上海海事大学2017年拟录取硕士研究生名单公示")

    tfidf_sentiment = get_tfidf(text_seg, Dict["sentiment"])
    tfidf_classification = get_tfidf(text_seg, Dict["classification"])

    sentimentResult = get_predictedResult(tfidf_sentiment, Dict["sentiment"])
    classificationResult = get_predictedResult(tfidf_classification, Dict["classification"])

    print "待分类预测文本:'上海海事大学2017年拟录取硕士研究生名单公示' 的分类结果为:\n 情感分类:{0}\n 类别分类:{1}\n".format(sentimentResult,classificationResult)


main()