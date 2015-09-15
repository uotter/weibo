__author__ = 'M'
# -*-coding:UTF-8-*-

import jieba
import string
import scipy as sp
import numpy as np

f_train = open(".//data//weibo_train_data//weibo_train_data.txt")  # 返回一个文件对象
f_test = open(".//data//weibo_predict_data//weibo_predict_data.txt")
stop_words_file_c = open(".//dic//stopwords_c.txt")
stop_words_file_e = open(".//dic//stopwords_e.txt")

stopword_c = stop_words_file_c.readline().decode("utf-8")
stop_words_c = []
while stopword_c:
    stop_words_c.append(stopword_c.strip('\n'))
    stopword_c = stop_words_file_c.readline().decode("utf-8")

# 使用的特征向量中的几个主要特征说明
# 特征向量 v = v1, v2
# v1: 微博的用户id