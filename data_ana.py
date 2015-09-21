import io_weibo
import util

__author__ = 'M'


def caculate_userids_proportion(train_lines, test_lines):
    total_test_num = len(test_lines)
    userids = set()

    for lines in train_lines:
        single_line = lines.decode("utf-8").split('\t')
        userid = single_line[0]
        userids.add(userid)

    count = 0
    for lines in test_lines:
        single_line = lines.decode("utf-8").split('\t')
        userid = single_line[0]
        if userid in userids:
            count += 1

    print count, total_test_num, (float(count) / float(total_test_num)), len(userids), len(train_lines)


def get_target_distribution(train_lines):
    dic_f = {}
    dic_c = {}
    dic_l = {}
    total_num = len(train_lines)
    for line in train_lines:
        single_line = line.decode("utf-8").split('\t')
        f_num = single_line[3]
        c_num = single_line[4]
        l_num = single_line[5]
        if dic_f.has_key(f_num):
            dic_f[f_num] += 1
        else:
            dic_f[f_num] = 1
        if dic_c.has_key(c_num):
            dic_c[c_num] += 1
        else:
            dic_c[c_num] = 1
        if dic_l.has_key(l_num):
            dic_l[l_num] += 1
        else:
            dic_l[l_num] = 1
    f_key_list = util.sort_by_value_dec(dic_f)
    c_key_list = util.sort_by_value_dec(dic_c)
    l_key_list = util.sort_by_value_dec(dic_l)
    write_list = ['-----------------forward analysis-----------------\n']
    for key in f_key_list:
        write_list.append(str(key) + ': ' + str(dic_f[key]) + ' with ' + str(float(dic_f[key]) / float(total_num))+'\n')
    write_list.append("-----------------comment analysis-----------------\n")
    for key in c_key_list:
        write_list.append(str(key) + ': ' + str(dic_c[key]) + ' with ' + str(float(dic_c[key]) / float(total_num))+'\n')
    write_list.append("-----------------like analysis-----------------\n")
    for key in l_key_list:
        write_list.append(str(key) + ': ' + str(dic_l[key]) + ' with ' + str(float(dic_l[key]) / float(total_num))+'\n')
    write_file = open('./target_num_percent.txt', 'w')
    write_file.writelines(write_list)
    write_file.close()


f_train = open(".//data//weibo_train_data//weibo_train_data_new.txt")
f_test = open(".//data//weibo_predict_data//weibo_predict_data_new.txt")

train_lines = f_train.readlines()
test_lines = f_test.readlines()
get_target_distribution(train_lines)
