#!/usr/bin/env python
# -*-coding=utf-8-*-


import os
from gensim import corpora, models, similarities


def getFileList(dir):
    return [dir + x for x in os.listdir(dir)]


dictLists = getFileList('./dict/')


class LoadDictionary(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __iter__(self):
        for dictFile in dictLists:
            sFileRaw, sFilePostfix = os.path.splitext(dictFile)
            sFileDir, sFileName = os.path.split(sFileRaw)
            (dictFile, corpusFile) = ('./dict/' + sFileName + '.dict', './corpus/' + sFileName + '.mm')
            yield self.dictionary.load_from_text(dictFile)


class LoadCorpus(object):
    def __iter__(self):
        for dictFile in dictLists:
            sFileRaw, sFilePostfix = os.path.splitext(dictFile)
            sFileDir, sFileName = os.path.split(sFileRaw)
            (dictFile, corpusFile) = ('./dict/' + sFileName + '.dict', './corpus/' + sFileName + '.mm')
            yield corpora.MmCorpus(corpusFile)


"""
    Ԥ����(easy_install nltk)
"""


# �򻯵� ����+Ӣ�� Ԥ����
def pre_process_cn(inputs, low_freq_filter=True):
    """
        1.ȥ��ͣ�ô�
        2.ȥ��������
        3.����Ϊ�ʸ�
        4.ȥ����Ƶ��

    """
    import nltk
    import jieba.analyse
    from nltk.tokenize import word_tokenize

    texts_tokenized = []
    for document in inputs:
        texts_tokenized_tmp = []
        for word in word_tokenize(document):
            texts_tokenized_tmp += jieba.analyse.extract_tags(word, 10)
        texts_tokenized.append(texts_tokenized_tmp)

    texts_filtered_stopwords = texts_tokenized

    # ȥ��������
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    texts_filtered = [[word for word in document if not word in english_punctuations] for document in
                      texts_filtered_stopwords]

    # �ʸɻ�
    from nltk.stem.lancaster import LancasterStemmer
    st = LancasterStemmer()
    texts_stemmed = [[st.stem(word) for word in docment] for docment in texts_filtered]

    # ȥ������Ƶ��
    if low_freq_filter:
        all_stems = sum(texts_stemmed, [])
        stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
        texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]
    else:
        texts = texts_stemmed
    return texts


dictionary = corpora.dictionary.Dictionary()
dictionary_memory_friendly = LoadDictionary(dictionary)
for vector in dictionary_memory_friendly:
    dictionary = vector

corpus = []
corpus_memory_friendly = LoadCorpus()
for vector in corpus_memory_friendly:
    corpus.append(vector[0])

if 0 < len(corpus):
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    model = models.LsiModel(corpus_tfidf, id2word=None, num_topics=20,
                            chunksize=2000000)  # ��ָ�� id2word=dictionary ʱ��LsiModel�ڲ������ corpus �ؽ� dictionary
    index = similarities.Similarity('./novel_', model[corpus], num_features=len(corpus))

    # Ҫ����Ķ���ǳ�����������С˵�н�ȡ��һ�λ�
    target_courses = ['�����ǵ����ϳ��ض�������������ɴ��Ů�������Ƿ����϶������Ŀ������������ޱ�רע�ؿ���ǰ������֤һ��������������ս��']
    target_text = pre_process_cn(target_courses, low_freq_filter=False)

    """
    �Ծ���������ƶ�ƥ��
    """
    # ѡ��һ����׼����
    ml_course = target_text[0]
    # �ʴ�����
    ml_bow = dictionary.doc2bow(ml_course)

    # ������ѡ���ģ������ lsi model �У���������������������ƶ�
    ml_lsi = model[ml_bow]  # ml_lsi ��ʽ�� (topic_id, topic_value)
    sims = index[ml_lsi]  # sims �����ս���ˣ� index[xxx] �������÷��� __getitem__() ������ml_lsi

    # ����Ϊ�������
    sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])

    # �鿴���
    print sort_sims[0:10]
    print len(dictLists)
    print dictLists[sort_sims[1][0]]
    print dictLists[sort_sims[2][0]]
    print dictLists[sort_sims[3][0]]
