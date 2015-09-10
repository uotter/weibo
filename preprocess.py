# -*-coding:UTF-8-*-
__author__ = 'Moore'
import nltk
import jieba
import string
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

f_train = open("C://tianchi//weibo201508//weibo_train_data//weibo_train_data.txt")  # 返回一个文件对象
i = 0
line = f_train.readline().decode("utf-8")  # 调用文件的 readline()方法
# lines = f.readlines()
train_lines_num = len(f_train.readlines())
print "total lines = ", train_lines_num
f_train.seek(0, 0)
stop_words_file_c = open("C://tianchi//weibo201508//stopwords_c.txt")
stop_words_file_e = open("C://tianchi//weibo201508//stopwords_e.txt")

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


def tfidf_compute_train(corpus_file, weiboindex, category, readsize):
    lines = corpus_file.readlines(readsize)
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


def tfidf_compute_test(test_file, weiboindex, readsize):
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


corpussize = 100
featuresets = tfidf_compute_train(f_train, 6, "comment", corpussize)
trainset, testset = featuresets[int(corpussize * 0.1):], featuresets[:int(corpussize * 0.1)]
classifier = nltk.NaiveBayesClassifier.train(trainset)
# print type(classifier.classify(testset))
print 'accuracy =', nltk.classify.accuracy(classifier, testset)

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
