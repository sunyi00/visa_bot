# check visa status, classify questions, decide whether it's about status check
# -*- coding:utf8 -*-

from pickle import load, dump
import jieba
from sklearn import linear_model, svm
from sklearn.externals import joblib
from numpy import array, zeros
from consts import VISA_PROGRESS_KEY_WORDS


WORD_BAG = load(open("word_bag.pkl"))
L = len(WORD_BAG)
N = len(VISA_PROGRESS_KEY_WORDS)
CASE_QUERY = {}

def retrieve():
	train = []
	target = []
	corpus = open("status_query.txt").read().split("\n")[:-1]
	load_training_data_kw(corpus, train, target, 1)
	corpus = open("fake_query.txt").read().split("\n")[:-1]
	load_training_data_kw(corpus, train, target, 0)
	return train, target

def load_training_data_index(corpus, train, target, value):
	for sentence in corpus:
		case = zeros(L)
		for x in jieba.cut_for_search(sentence):
			i = WORD_BAG.get(x)
			if i is not None:
				case[i] = 1
		train.append(case)
		target.append(value)
		CASE_QUERY[tuple(case)] = sentence

def load_training_data_kw(corpus, train, target, value):
	for sentence in corpus:
		case = zeros(N)
		for kw, pair in VISA_PROGRESS_KEY_WORDS.iteritems():
			if kw in sentence:
				i, x = pair
				case[i] = x
		train.append(case)
		target.append(value)
		CASE_QUERY[tuple(case)] = sentence
 

def training(train, target):
	clf = svm.SVC()
	clf.fit(train, target)
	for case, t in zip(train, target):
		p = clf.predict([case])
		if p[0] != t:
			print CASE_QUERY.get(tuple(case)), t
	joblib.dump(clf, "status_check_svm.pkl")

def vectorize(sentence):
	case = zeros(N)
	for kw, pair in VISA_PROGRESS_KEY_WORDS.iteritems():
		if kw in sentence:
			i, x = pair
			case[i] = x
	return case

if __name__ == "__main__":

#	train, target = retrieve()
#	training(train, target)

	clf = joblib.load("status_check_svm.pkl")	
	question = ""
	while question != "q":
		question = raw_input("请输入您的问题(q 退出)>>> ")
		case = vectorize(question)
		p = clf.predict([case])
		print p
