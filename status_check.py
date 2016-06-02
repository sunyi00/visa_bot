# check visa status, classify questions, decide whether it's about status check
# -*- coding:utf8 -*-

from pickle import load, dump
import jieba
from sklearn import linear_model, svm
from sklearn.externals import joblib
from numpy import array, zeros
from consts import VISA_PROGRESS_KEY_WORDS


N = len(VISA_PROGRESS_KEY_WORDS)
CASE_QUERY = {}


def vectorize(sentence):
	case = zeros(N)
	for kw, pair in VISA_PROGRESS_KEY_WORDS.iteritems():
		if kw in sentence:
			i, x = pair
			case[i] = x
	return case

if __name__ == "__main__":


	clf = joblib.load("status_check_svm.pkl")	
	question = ""
	while question != "q":
		question = raw_input("请输入您的问题(q 退出)>>> ")
		case = vectorize(question)
		p = clf.predict([case])
		print p
