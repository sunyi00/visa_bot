# corpus index, a fast and dirty implementation
# -*- coding:utf8 -*-

import jieba
from pickle import load, dump

def load_corpus():
	corpus = open("status_query.txt").read().split("\n")[:-1]
	corpus.extend(open("fake_query.txt").read().split("\n")[:-1])
#	corpus.extend(open("visa_chat_20160320.txt").read().split("\n")[:-1])
	return corpus

def word_index(corpus):
	word_bag = set([])
	for sentence  in corpus:
		for x in jieba.cut_for_search(sentence):
			word_bag.add(x)
	print "total %d distinctive words"%len(word_bag)
	word_bag = dict([(x, i) for i, x in enumerate(sorted(list(word_bag)))])
	dump(word_bag, open("word_bag.pkl", "w"))


if __name__ == "__main__":
	corpus = load_corpus()
	word_index(corpus)
	
