# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv as csv
from sklearn.naive_bayes import MultinomialNB
import numpy as np 
from pyvi.pyvi import ViTokenizer, ViPosTagger
import sys
import pickle

def read(filename):
        f = open(filename)
        data = pickle.load(f)
        f.close()
        return data

def makeMatrix(arr,dct):
    lst = []
    for x in dct:
        if x in arr:
            lst.append(1)
        else:
            lst.append(0)
    return lst
count = 0
with open('data.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        count = count + 1
        if count == 2 :
            pre = unicode(row[0], "utf-8")

diction = read("diction.file")

# du doan
pre = pre.replace("," , "").replace("." , "")
pre = ViTokenizer.tokenize(pre)
pre = pre.lower()
arrpre = pre.split()
apre = makeMatrix(arrpre, diction)
dpre = np.array([apre])

lb = read("labels.file")

trd = read("trains.file")

## call MultinomialNB
clf = MultinomialNB()
# training 
clf.fit(trd, lb)

# test
print(repr(pre).decode("unicode-escape"))
print('Predicting class of dpre:', str(clf.predict(dpre)[0]), clf.predict_proba(dpre))