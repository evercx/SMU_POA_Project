# -*- coding:utf-8 -*-

import ConfigParser
import os

# 获取config配置文件

def getConfig(section,key):

    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/app.conf'       #os.path.split(os.path.realpath(__file__))[0]得到当前文件模块的目录
    config.read(path)
    return config.get(section,key)

def get_University_list():

     return [
                {
                    "chn_name": "上海海事大学",
                    "en_name": "smu"
                },

                {
                    "chn_name": "上海交通大学",
                    "en_name": "sjtu"
                },

                {
                    "chn_name": "同济大学",
                    "en_name": "tongji"
                },

                {
                    "chn_name": "复旦大学",
                    "en_name": "fudan"
                },

                {
                    "chn_name": "华东师范大学",
                    "en_name": "ecnu"
                },

                {
                    "chn_name": "上海大学",
                    "en_name": "shu"
                },

                {
                    "chn_name": "华东理工大学",
                    "en_name": "ecust"
                },

                {
                    "chn_name": "东华大学",
                    "en_name": "dhu"
                },

                {
                    "chn_name": "上海财经大学",
                    "en_name": "shufe"
                },

                {
                    "chn_name": "上海外国语大学",
                    "en_name": "shisu"
                },

                {
                    "chn_name": "华东政法大学",
                    "en_name": "ecupl"
                },

                {
                    "chn_name": "上海师范大学",
                    "en_name": "shnu"
                },

                {
                    "chn_name": "上海理工大学",
                    "en_name": "usst"
                },

                {
                    "chn_name": "上海海洋大学",
                    "en_name": "shou"
                },

                {
                    "chn_name": "上海中医药大学",
                    "en_name": "shutcm"
                },

                {
                    "chn_name": "上海音乐学院",
                    "en_name": "sus"
                },

                {
                    "chn_name": "上海戏剧学院",
                    "en_name": "sta"
                },

                {
                    "chn_name": "上海对外经贸大学",
                    "en_name": "shift"
                },

                {
                    "chn_name": "上海电机学院",
                    "en_name": "sdju"
                },

                {
                    "chn_name": "上海工程技术大学",
                    "en_name": "sues"
                }
            ]
