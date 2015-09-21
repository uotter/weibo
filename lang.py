# -*-coding:UTF-8-*-
__author__ = 'Moore'

import jieba
import string
import io_weibo
from sklearn.feature_extraction.text import TfidfVectorizer
import time


def target_map(num):
    num = int(num)
    if num == 0:
        return 0
    elif 0 < num:
        return 1
    # elif 100 < num <= 100:
    #     return 2
    # elif 10 < num <= 15:
    #     return 3
    # else:
    #     return 4


def return_target_map(num, userid_num):
    userid_num = int(userid_num)
    num = int(num)
    if num == 0:
        return 0
    elif num == 1:
        return userid_num
    #     if 0 < userid_num <= 5:
    #         return userid_num
    #     else:
    #         return 5
    # elif num == 2:
    #     if 5 < userid_num <= 10:
    #         return userid_num
    #     elif userid_num <= 5:
    #         return 5
    #     else:
    #         return 10
    # elif num == 3:
    #     if 10 < userid_num <= 15:
    #         return userid_num
    #     elif userid_num <= 10:
    #         return 10
    #     else:
    #         return 15
    # else:
    #     if userid_num <= 16:
    #         return 16
    #     else:
    #         return userid_num


def preprocess(weibo_str):
    if weibo_str.find("http"):
        start = weibo_str.find("http")
        remove_str = weibo_str[start:start + 19]
        return weibo_str.replace(remove_str, "")
    else:
        return weibo_str


def file_to_arr(lines, text_index, train_or_test):
    start = time.time()
    stop_words_file_c = io_weibo.stop_words_file_c
    stopword_c = stop_words_file_c.readline().decode("utf-8")
    stop_words_c = []
    while stopword_c:
        stop_words_c.append(stopword_c.strip('\n'))
        stopword_c = stop_words_file_c.readline().decode("utf-8")
    end = time.time()
    # print 'stop words read fininshed with: ' + str(end - start)
    start = time.time()
    train_like = []
    train_comment = []
    train_forward = []
    corpus = []
    start_inside = time.time()
    train_total_num = len(lines)
    for index in range(len(lines)):
        single_line = lines[index].decode("utf-8").split('\t')
        str_without_http = preprocess(single_line[text_index].replace("\n", "").replace(" ", ""))
        if str_without_http is not None:
            seg_list = jieba.cut(str_without_http)
            seg_result = []
            for orginal_word in seg_list:
                if orginal_word not in stop_words_c and filter(lambda c: c not in string.letters, orginal_word):
                    seg_result.append(orginal_word)
            if len(seg_result) != 0:
                corpus.append(' '.join(seg_result))
                if train_or_test == 'train':
                    train_forward.append(target_map(single_line[3]))
                    train_comment.append(target_map(single_line[4]))
                    train_like.append(target_map(single_line[5]))
            else:
                corpus.append('no_features')
                if train_or_test == 'train':
                    train_forward.append(target_map(single_line[3]))
                    train_comment.append(target_map(single_line[4]))
                    train_like.append(target_map(single_line[5]))
        else:
            corpus.append('no_features')
            if train_or_test == 'train':
                train_forward.append(target_map(single_line[3]))
                train_comment.append(target_map(single_line[4]))
                train_like.append(target_map(single_line[5]))
        if index % 1000 == 0:
            end_inside = time.time()
            print 'NO. ' + str(index) + ' for ' + train_or_test + ' completed with ' + str(
                (end_inside - start_inside)) + 's, and  still left ' + str(
                train_total_num - index) + ' with ' + str(
                (end_inside - start_inside) * (train_total_num - index) / 1000) + 's'
            start_inside = time.time()
    end = time.time()
    print 'segmentation for ' + train_or_test + ' fininshed with: ' + str(end - start)
    if train_or_test == 'train':
        return corpus, train_forward, train_comment, train_like
    else:
        return corpus


def feature_tfidf(train_lines, test_lines, train_text_index, test_text_index):
    start = time.time()
    train_text_arr, forward_train, comment_train, like_train = file_to_arr(train_lines, train_text_index, 'train')

    test_text_arr = file_to_arr(test_lines, test_text_index, 'test')
    end = time.time()
    print 'train and test file to array fininshed with: ' + str(end - start)
    start = time.time()
    # debug start
    # train_text_arr_nozero = []
    # comment_train_nozero = []
    # for i in range(len(comment_train)):
    #     if int(comment_train[i]) != 0:
    #         train_text_arr_nozero.append(train_text_arr[i])
    #         comment_train_nozero.append(comment_train[i])
    # train_text_arr = train_text_arr_nozero
    # comment_train = comment_train_nozero
    # debug end

    tv = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
    tfidf_train = tv.fit_transform(train_text_arr)
    tv2 = TfidfVectorizer(vocabulary=tv.vocabulary_)
    tfidf_test = tv2.fit_transform(test_text_arr)
    end = time.time()
    print 'train and test array to tfidf feature fininshed with: ' + str(end - start)
    return tfidf_train, tfidf_test, forward_train, comment_train, like_train
