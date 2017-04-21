# -*- coding:utf-8 -*-
# 对分完词的文本用tf-idf提取文本特征,并进行模型训练

from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import  cPickle as pickle
import mod_config

def readFile(path):

    f = open(path,"r")
    content = f.read()
    f.close()
    return content




def writeBunchObj(path,bunchobj):

    file_Obj = open(path,"wb")
    pickle.dump(bunchobj,file_Obj)
    file_Obj.close()


def get_dataBunch(typeDict):


    train_data = load_files(typeDict["load_Files_Path"],categories=typeDict["categories"])
    return train_data


def extract_tfidf(train_data,typeDict):

    #词语计数

    stopwordlist = readFile("./hlt_stop_words.txt").splitlines()
    count_vect = CountVectorizer(stop_words=stopwordlist,max_df=0.5)
    X_train_counts = count_vect.fit_transform(train_data.data)


    #print "训练数据共有{0}篇,词汇计数为{1}个".format(X_train_counts.shape[0],X_train_counts.shape[1])
    #print count_vect.vocabulary_.get(u'海事')

    #TF-IDF提取文本特征
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    writeBunchObj(typeDict["count_vect_Path"], count_vect)
    writeBunchObj(typeDict["tfidf_Path"], tfidf_transformer)

    return X_train_tfidf


def train_sentiment_model(X_train_tfidf,train_data):

    clf = MultinomialNB(alpha=0.1).fit(X_train_tfidf,train_data.target)

    return clf




def main():

    #typeDict = mod_config.get_ModelType_Info()["sentiment"]
    typeDict = mod_config.get_ModelType_Info()["classification"]

    train_data = get_dataBunch(typeDict)
    X_train_tfidf = extract_tfidf(train_data,typeDict)

    clf = train_sentiment_model(X_train_tfidf,train_data)

    joblib.dump(clf,typeDict["save_model_Path"]);
    print "模型保存成功"


main()
