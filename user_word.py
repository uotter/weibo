__author__ = 'M'
# -*-coding:UTF-8-*-

import jieba
import string
import scipy as sp
import numpy as np

f_train = open(".//data//weibo_train_data//weibo_train_data.txt")  # ����һ���ļ�����
f_test = open(".//data//weibo_predict_data//weibo_predict_data.txt")
stop_words_file_c = open(".//dic//stopwords_c.txt")
stop_words_file_e = open(".//dic//stopwords_e.txt")

stopword_c = stop_words_file_c.readline().decode("utf-8")
stop_words_c = []
while stopword_c:
    stop_words_c.append(stopword_c.strip('\n'))
    stopword_c = stop_words_file_c.readline().decode("utf-8")

# ʹ�õ����������еļ�����Ҫ����˵��
# �������� v = v1, v2
# v1: ΢�����û�id