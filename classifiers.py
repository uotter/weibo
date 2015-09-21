__author__ = 'Moore'

from sklearn.naive_bayes import MultinomialNB
import time
import lang


def mnbclf_compute(train_file, test_file, train_text_index, test_text_index):
    start = time.time()
    tfidf_train, tfidf_test, forward_train, comment_train, like_train = lang.feature_tfidf(train_file, test_file,
                                                                                           train_text_index,
                                                                                           test_text_index)
    end = time.time()
    print 'compute tfidf fininshed with: ' + str(end - start)
    start = time.time()
    clf_forward = MultinomialNB().fit(tfidf_train, forward_train)
    clf_comment = MultinomialNB().fit(tfidf_train, comment_train)
    clf_like = MultinomialNB().fit(tfidf_train, like_train)
    end = time.time()
    print 'train the classifiers fininshed with: ' + str(end - start)
    start = time.time()
    forward_class_predicted = clf_forward.predict(tfidf_test)
    comment_class_predicted = clf_comment.predict(tfidf_test)
    like_class_predicted = clf_like.predict(tfidf_test)
    end = time.time()
    print 'predict fininshed with: ' + str(end - start)
    return forward_class_predicted, comment_class_predicted, like_class_predicted
