# -*- coding:utf-8 -*-
# 对训练数据进行分词操作

import os
import jieba
import codecs



def readFile(path):

    f = open(path,"r")
    content = f.read()
    f.close()
    return content

def writeFile(savePath,content):

    try:

        f = codecs.open(savePath, 'w', "utf-8")
        f.write(content)

    except Exception, e:
        print e
        print savePath + "  写入失败"

    finally:
        if f:
            f.close()


def seg_traindata():

    traindataPath = "./sentiment_train_data/"
    segdataPath = "./sentiment_seg_data/"

    for dir in os.listdir(traindataPath):
        print dir
        if dir == ".DS_Store":
            os.remove(traindataPath+".DS_Store")
            continue

        read_Class_Path = traindataPath + dir + "/"
        seg_Class_dir = segdataPath + dir + "/"

        if not os.path.exists(seg_Class_dir):
            os.makedirs(seg_Class_dir)

        for fileName in os.listdir(read_Class_Path):

            readFullFilePath = read_Class_Path + fileName
            saveFullFilePath = seg_Class_dir + fileName

            newsBody = readFile(readFullFilePath).strip().replace("\r\n","").strip()
            newsBody_seg = " ".join(jieba.cut(newsBody))
            writeFile(saveFullFilePath,newsBody_seg)


def main():

    seg_traindata()
    print "中文分词成功"


main()
