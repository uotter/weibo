__author__ = 'M'

f_train = open(".//data//weibo_train_data//weibo_train_data.txt")
f_test = open(".//data//weibo_predict_data//weibo_predict_data.txt")
train_lines = f_train.readlines()
test_lines = f_test.readlines()

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

print count, total_test_num, (float(count)/float(total_test_num)), len(userids)
