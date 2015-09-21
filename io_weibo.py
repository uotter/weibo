# -*-coding:UTF-8-*-
import time
import random

__author__ = 'M'

f_train = open(".//data//weibo_train_data//weibo_train_data_new.txt")
f_test = open(".//data//weibo_predict_data//weibo_predict_data_new.txt")
stop_words_file_c = open(".//dic//stopwords_c.txt")
stop_words_file_e = open(".//dic//stopwords_e.txt")


def read_train_test():
    start = time.time()
    f_train_lines = f_train.readlines()
    end = time.time()
    print 'read train file fininshed with: ' + str(end - start)
    start = time.time()
    f_test_lines = f_test.readlines()
    end = time.time()
    print 'read test file fininshed with: ' + str(end - start)
    return f_train_lines, f_test_lines


def random_only_train(total_num, test_size):
    start = time.time()
    f_train_lines = f_train.readlines()
    if total_num >= 1:
        f_train_lines = f_train_lines[:total_num]
    end = time.time()
    print 'read train file fininshed with: ' + str(end - start)
    start = time.time()
    f_train_size = len(f_train_lines)
    # ��list�������ȡ���ɸ�Ԫ�أ���Ϊһ��Ƭ�Ϸ���
    random_test_lines = random.sample(f_train_lines, int(f_train_size * test_size))
    random_train_lines = list(set(f_train_lines) - set(random_test_lines))
    end = time.time()
    print 'random train and test files fininshed with: ' + str(end - start)
    print 'size of random_train_lines is ' + str(len(random_train_lines)) + ' and size of random_test_lines is ' + str(
        len(random_test_lines)) + '.'
    return random_train_lines, random_test_lines


def write_format_result(test_userid_value, filename):
    start = time.time()
    f_result = open(filename + '.txt', 'w')
    f_result.writelines(test_userid_value)
    f_result.close()
    end = time.time()
    print 'write result file fininshed with: ' + str(end - start)


def write_format_testtrue(random_test_lines, filename):
    start = time.time()
    random_test_value = []
    for line in random_test_lines:
        single_line = line.decode("utf-8").split('\t')
        userid = single_line[0]
        weiboid = single_line[1]
        out_str = userid + '\t' + weiboid + '\t'
        out_f = single_line[3]
        out_c = single_line[4]
        out_l = single_line[5]
        out_str = out_str + str(out_f) + ',' + str(out_c) + ',' + str(out_l) + '\n'
        random_test_value.append(out_str)
    f_result = open(filename + '.txt', 'w')
    f_result.writelines(random_test_value)
    f_result.close()
    end = time.time()
    print 'write random_test_lines result with format fininshed with: ' + str(end - start)


def read_result_for_evaluation(predict_filename, true_filename):
    f_predict = open(".//" + predict_filename + '.txt')
    f_true = open(".//" + true_filename + '.txt')
    return f_predict.readlines(), f_true.readlines()
