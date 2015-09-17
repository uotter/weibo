__author__ = 'M'

f_test = open(".//data//weibo_predict_data//weibo_predict_data_new.txt")
lines = f_test.readlines()
test_baseline = []
for index in range(len(lines)):
    single_line = lines[index].decode("utf-8").split('\t')
    str_new = single_line[0] + '\t' + single_line[1] + '\t0,0,0\n'
    test_baseline.append(str_new)
f_result = open('baseline_new.txt', 'w')
f_result.writelines(test_baseline)
f_result.close()
