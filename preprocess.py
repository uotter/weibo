# -*-coding:UTF-8-*-
__author__ = 'Moore'
import nltk
import jieba
import string
import scipy as sp
import numpy as np
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import classification_report

f_train = open(".//data//weibo_train_data//weibo_train_data.txt")  # 返回一个文件对象
f_test = open(".//data//weibo_predict_data//weibo_predict_data.txt")
# i = 0
# line = f_train.readline().decode("utf-8")  # 调用文件的 readline()方法
# # lines = f.readlines()
# train_lines_num = len(f_train.readlines())
# print "total lines = ", train_lines_num
# f_train.seek(0, 0)
stop_words_file_c = open(".//dic//stopwords_c.txt")
stop_words_file_e = open(".//dic//stopwords_e.txt")

stopword_c = stop_words_file_c.readline().decode("utf-8")
stop_words_c = []
while stopword_c:
    stop_words_c.append(stopword_c.strip('\n'))
    stopword_c = stop_words_file_c.readline().decode("utf-8")


# for word in stop_words_c:
#     print word
# stopword_e = stop_words_file_e.readline().decode("utf-8")
# stop_words_e = []
# while stopword_e:
#     stop_words_e.append(stopword_e)
#     stopword_e = stop_words_file_e.readline()
# for word in stop_words_e:
#     print word




def preprocess(weibo_str):
    if weibo_str.find("http"):
        start = weibo_str.find("http")
        remove_str = weibo_str[start:start + 19]
        return weibo_str.replace(remove_str, "")
    else:
        weibo_str


def get_words(weibo_str):
    item_words_dic = {}
    seg_list = jieba.cut(weibo_str)
    for orginal_word in seg_list:
        if orginal_word not in stop_words_c:
            if filter(lambda c: c not in string.letters, orginal_word):
                if orginal_word in item_words_dic.keys():
                    countnum = item_words_dic.keys().count(orginal_word)
                    item_words_dic[orginal_word] = countnum + 1
                else:
                    item_words_dic[orginal_word] = 1
    return item_words_dic


def file_to_arr(lines, text_index, train_or_test):
    train_like = []
    train_comment = []
    train_forward = []
    corpus = []
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
                    train_forward.append(single_line[3])
                    train_comment.append(single_line[4])
                    train_like.append(single_line[5])
            else:
                corpus.append('no_features')
                if train_or_test == 'train':
                    train_forward.append(single_line[3])
                    train_comment.append(single_line[4])
                    train_like.append(single_line[5])
        else:
            corpus.append('no_features')
            if train_or_test == 'train':
                train_forward.append(single_line[3])
                train_comment.append(single_line[4])
                train_like.append(single_line[5])
    if train_or_test == 'train':
        return corpus, train_forward, train_comment, train_like
    else:
        return corpus


def mnbclf_compute(train_file, test_file, train_text_index, test_text_index, train_read_size, test_read_size):
    total_train_lines = train_file.readlines()
    total_test_lines = test_file.readlines()
    if train_read_size == -1:
        train_lines = total_train_lines
    else:
        train_lines = total_train_lines[:train_read_size]

    train_size = len(train_lines)

    if test_read_size == -1:
        test_lines = total_test_lines
    else:
        test_lines = total_test_lines[:test_read_size]
    test_size = len(test_lines)

    train_text_arr, forward_train, comment_train, like_train = file_to_arr(train_lines, train_text_index, 'train')
    test_text_arr = file_to_arr(test_lines, test_text_index, 'test')

    tv = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
    tfidf_train = tv.fit_transform(train_text_arr)
    tv2 = TfidfVectorizer(vocabulary=tv.vocabulary_)
    tfidf_test = tv2.fit_transform(test_text_arr)
    # x_train, x_test, y_train, y_test = train_test_split(tfidf_train, forward_train, test_size=0.2)
    # clf = MultinomialNB().fit(x_train, y_train)
    clf = MultinomialNB().fit(tfidf_train, forward_train)
    # clf_forward = MultinomialNB().fit(tfidf_train, forward_train)
    # clf_comment = MultinomialNB().fit(tfidf_train, comment_train)
    # clf_like = MultinomialNB().fit(tfidf_train, like_train)

    doc_class_predicted = clf.predict(tfidf_test)
    return doc_class_predicted
    # print(doc_class_predicted)
    # print(np.mean(doc_class_predicted == y_test))


def tfidf_compute(corpus_file, test_file, weiboindex, readsize, testreadsize):
    total_train_lines = corpus_file.readlines()
    total_test_lines = test_file.readlines()
    if readsize == -1:
        lines = total_train_lines
    else:
        lines = total_train_lines[:readsize]

    train_size = len(lines)

    if testreadsize == -1:
        test_lines = total_test_lines
    else:
        test_lines = total_test_lines[:testreadsize]
    test_size = len(test_lines)

    lines.extend(test_lines)

    corpus = []
    for index in range(len(lines)):
        single_line = lines[index].decode("utf-8").split('\t')
        if index < train_size:
            str_without_http = preprocess(single_line[weiboindex].replace("\n", "").replace(" ", ""))
        else:
            str_without_http = preprocess(single_line[3].replace("\n", "").replace(" ", ""))
        if str_without_http is not None:
            seg_list = jieba.cut(str_without_http)
            seg_result = []
            for orginal_word in seg_list:
                if orginal_word not in stop_words_c and filter(lambda c: c not in string.letters, orginal_word):
                    seg_result.append(orginal_word)
            corpus.append(' '.join(seg_result))

    tv = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words=stopword_c)
    tfidf_train_2 = tv.fit_transform(corpus)
    tv2 = TfidfVectorizer(vocabulary=tv.vocabulary_)
    tfidf_test_2 = tv2.fit_transform(newsgroups_test.data)

    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    print tfidf
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

    trainset_like_para = []
    trainset_forward_para = []
    trainset_comment_para = []

    testset_para = []
    test_textid_userid_para = []

    for i in range(len(weight)):  # 打印每个文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        single_line = lines[i].decode("utf-8").split('\t')
        if i < train_size:
            like = single_line[5]
            forward = single_line[3]
            comment = single_line[4]
            features = {}
            print u"第", i, u"个训练文本的词语tf-idf权重计算完毕"
            for j in range(len(word)):
                features[word[j]] = weight[i][j]
                # print word[j], weight[i][j]
            trainset_like_para.append((features, like))
            trainset_forward_para.append((features, forward))
            trainset_comment_para.append((features, comment))
        else:
            features = {}
            textid = single_line[0]
            userid = single_line[1]
            print u"第", (i - train_size), u"个测试文本的词语tf-idf权重计算完毕"
            for j in range(len(word)):
                features[word[j]] = weight[i][j]
            testset_para.append(features)
            test_textid_userid_para.append(textid + '\t' + userid + '\t')

    return trainset_like_para, trainset_forward_para, trainset_comment_para, testset_para, test_textid_userid_para


def tfidf_compute_test(test_file, category, weiboindex, readsize):
    lines = test_file.readlines(readsize)
    corpus = []
    featuresets = []

    for single_line in lines:
        single_line = single_line.decode("utf-8").split('\t')
        str_without_http = preprocess(single_line[weiboindex].replace("\n", "").replace(" ", ""))
        if str_without_http is not None:
            seg_list = jieba.cut(str_without_http)
            seg_result = []
            for orginal_word in seg_list:
                if orginal_word not in stop_words_c and filter(lambda c: c not in string.letters, orginal_word):
                    seg_result.append(orginal_word)
            corpus.append(' '.join(seg_result))
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    for i in range(len(weight)):  # 打印每个文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        single_line = lines[i].decode("utf-8").split('\t')
        like = single_line[5]
        forward = single_line[3]
        comment = single_line[4]
        features = {}
        print u"-------这里输出第", i, u"个文本的词语tf-idf权重------"
        for j in range(len(word)):
            features[word[j]] = weight[i][j]
            # print word[j], weight[i][j]
        if category == "like":
            featuresets.append((features, like))
        elif category == "forward":
            featuresets.append((features, forward))
        elif category == "comment":
            featuresets.append((features, comment))
    return featuresets


corpussize = 10000
testsize = -1
result = mnbclf_compute(f_train, f_test, 6, 3, corpussize, testsize)
print len(result)
outfile = open('./result.txt', 'w')
for idx in range(len(result)):
    outfile.write(str(idx) + ' ' + result[idx]+'\n')
outfile.close()

# trainset_like, trainset_forward, trainset_comment, testset, test_textid_userid = tfidf_compute(f_train, f_test, 6,
#                                                                                                corpussize, testsize)
# classifier_like = nltk.NaiveBayesClassifier.train(trainset_like)
# classifier_forward = nltk.NaiveBayesClassifier.train(trainset_forward)
# classifier_comment = nltk.NaiveBayesClassifier.train(trainset_comment)
#
# test_like_result = []
# test_forward_result = []
# test_comment_result = []
#
# for text in testset:
#     like_predict = classifier_like.classify(text)
#     forward_predict = classifier_forward.classify(text)
#     comment_predict = classifier_comment.classify(text)
#     test_like_result.append(like_predict)
#     test_forward_result.append(forward_predict)
#     test_comment_result.append(comment_predict)
#
# for i in range(len(test_like_result)):
#     print i, test_textid_userid[i] + str(test_like_result[i]) + ',' + str(test_forward_result[i]) + ',' + str(
#         test_comment_result[i])



# print type(classifier.classify(testset))
# print 'accuracy =', nltk.classify.accuracy(classifier, testset)

# single_line = lines[77].decode("utf-8").split('\t')
# str_without_http = preprocess(single_line[6].replace("\n", "").replace(" ", ""))
# print single_line
# print str_without_http
# word_elements = get_words(str_without_http)
# for word in word_elements.keys():
#     print i, word, word_elements[word]

# while i <= 100:
#     # print line
#     line = f.readline().decode("utf-8")
#     t = line.split('\t')
#     str_without_http = preprocess(t[6].replace("\n", "").replace(" ", ""))
#     if str_without_http is not None:
#         word_elements = get_words(str_without_http)
#         for word in word_elements.keys():
#             print i, word, word_elements[word]
#     i += 1

f_train.close()
