# -*-coding:UTF-8-*-
__author__ = 'M'

import time

f_train = open(".//data//weibo_train_data//weibo_train_data.txt")  # 返回一个文件对象
f_test = open(".//data//weibo_predict_data//weibo_predict_data.txt")


# stop_words_file_c = open(".//dic//stopwords_c.txt")
# stop_words_file_e = open(".//dic//stopwords_e.txt")
#
# stopword_c = stop_words_file_c.readline().decode("utf-8")
# stop_words_c = []
# while stopword_c:
#     stop_words_c.append(stopword_c.strip('\n'))
#     stopword_c = stop_words_file_c.readline().decode("utf-8")


def sort_by_value_dec(d):
    items = d.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort(reverse=True)
    return [backitems[index][1] for index in range(0, len(backitems))]


# 使用的特征向量中的几个主要特征说明
# 特征向量 v = v1, v2, v3, v4...
# v1: 微博的用户id在训练集中所发过的微博的平均转发、评论、点赞数
# v2, v3, v4...: 得到的转发、评论、点赞数最多的词汇的集合组成的特征词集，对于一个具体的特征向量，每个元素的值对应于该词在该语句中出现的次数，即tf

start = time.time()
f_train_lines = f_train.readlines()
end = time.time()
print 'read train file fininshed with: ' + str(end - start)
start = time.time()
f_test_lines = f_test.readlines()
end = time.time()
print 'read test file fininshed with: ' + str(end - start)

user_f = {}
user_c = {}
user_l = {}
user_count = {}
start = time.time()
for line in f_train_lines:
    single_line = line.decode("utf-8").split('\t')
    userid = single_line[0]
    f_num = int(single_line[3])
    c_num = int(single_line[4])
    l_num = int(single_line[5])
    user_count_current = 1
    if userid in user_count:
        user_count_current = user_count[userid]
        user_count[userid] += 1
    else:
        user_count[userid] = 1
    if userid in user_f.keys():
        user_f[userid] = (user_f[userid] + f_num) / user_count_current
    else:
        user_f[userid] = f_num / user_count_current
    if userid in user_c.keys():
        user_c[userid] = (user_c[userid] + c_num) / user_count_current
    else:
        user_c[userid] = c_num / user_count_current
    if userid in user_l.keys():
        user_l[userid] = (user_l[userid] + l_num) / user_count_current
    else:
        user_l[userid] = l_num / user_count_current
end = time.time()
print 'get user map fininshed with: ' + str(end - start)
test_userid_value = []
start = time.time()
for line in f_test_lines:
    single_line = line.decode("utf-8").split('\t')
    userid = single_line[0]
    weiboid = single_line[1]
    out_str = userid + '\t' + weiboid + '\t'
    out_f = 0
    out_c = 0
    out_l = 0
    if userid in user_f.keys():
        out_f = user_f[userid]
    if userid in user_c.keys():
        out_c = user_c[userid]
    if userid in user_l.keys():
        out_l = user_l[userid]

    out_str = out_str + str(out_f) + ',' + str(out_c) + ',' + str(out_l) + '\n'
    test_userid_value.append(out_str)
end = time.time()
print 'compute result fininshed with: ' + str(end - start)
f_result = open('user_value.txt', 'w')
f_result.writelines(test_userid_value)
f_result.close()


# corpus, train_forward, train_comment, train_like = pre.file_to_arr(f_train_lines, 6, "train")
#
# word_forward_map = {}
# word_comment_map = {}
# word_like_map = {}
# for i in range(len(corpus)):
#     text = corpus[i]
#     forward = train_forward[i]
#     comment = train_comment[i]
#     like = train_like[i]
#     for word in text and word != 'no_features':
#         if word in word_forward_map.keys():
#             old_forward_num = word_forward_map[word]
#             new_forward_num = old_forward_num + forward
#             word_forward_map[word] = new_forward_num
#         else:
#             word_forward_map[word] = forward
#         if word in word_comment_map.keys():
#             old_comment_num = word_comment_map[word]
#             new_comment_num = old_comment_num + comment
#             word_comment_map[word] = new_comment_num
#         else:
#             word_comment_map[word] = comment
#         if word in word_like_map.keys():
#             old_like_num = word_like_map[word]
#             new_like_num = old_like_num + like
#             word_like_map[word] = new_like_num
#         else:
#             word_like_map[word] = like
