# -*-coding:UTF-8-*-
import io_weibo
import user_word
import evaluation
import data_ana
import classifiers

__author__ = 'M'

f_train_lines, f_test_lines = io_weibo.read_train_test()
# f_train_lines, f_test_lines = io_weibo.random_only_train(200000, 0.2)

# data_ana.caculate_userids_proportion(f_train_lines,f_test_lines)
test_userid_value = user_word.user_only_add(f_train_lines, f_test_lines)
# test_userid_value = user_word.user_word(f_train_lines, f_test_lines)
# io_weibo.write_format_testtrue(f_test_lines, 'user_value_true_test1')
io_weibo.write_format_result(test_userid_value, 'user_value_test1')
# test_lines, true_lines = io_weibo.read_result_for_evaluation('user_value_test1', 'user_value_true_test1')
# precision_final = evaluation.evaluate(test_lines, true_lines)
# print 'final score: ' + str(precision_final)
