# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv as csv
from sklearn.naive_bayes import MultinomialNB
import numpy as np 
from pyvi.pyvi import ViTokenizer, ViPosTagger
import sys
import simplejson
import pickle

count = 0
arr = []
labels = []
dt = {}
allstr = ""

# Write and read function array to file
def write(data, outfile):
        f = open(outfile, "w+b")
        pickle.dump(data, f)
        f.close()
def read(filename):
        f = open(filename)
        data = pickle.load(f)
        f.close()
        return data

# Make matrix with a paper
def makeMatrix(arr,dct):
    lst = []
    for i in dct:
        temp = 0
        for x in arr:
            if x==i:
                temp = temp + 1
        lst.append(temp)

    # for x in dct:
    #     if x in arr:
    #         lst.append(1)
    #     else:
    #         lst.append(0)
    return lst

# Read data to predict
with open('data.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        count = count + 1
        if count == 2 :
            pre = unicode(row[0], "utf-8")

count = 0

# Read data to train
with open('dt500.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        count = count + 1
        
        if (count%2) == 1 :
            utf = unicode(row[0], "utf-8")
            allstr = allstr + utf
            arr.append(utf)
        else:
            st = row[0].strip('\n')
            st = st.strip('\r')
            st = st.strip('\n')
            labels.append(st)

count = 0
with open('dantrixhmini.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        count = count + 1
        
        if (count%2) == 1 :
            utf = unicode(row[0], "utf-8")
            allstr = allstr + utf
            arr.append(utf)
        else:
            st = row[0].strip('\n')
            st = st.strip('\r')
            st = st.strip('\n')
            labels.append(st)
# count = 0
# with open('dt100.csv') as csvDataFile:
#     csvReader = csv.reader(csvDataFile)
#     for row in csvReader:
#         count = count + 1
        
#         if (count%2) == 1 :
#             utf = unicode(row[0], "utf-8")
#             allstr = allstr + utf
#             arr.append(utf)
#         else:
#             st = row[0].strip('\n')
#             st = st.strip('\r')
#             st = st.strip('\n')
#             labels.append(st)
# count = 0
# with open('dtvnxh100.csv') as csvDataFile:
#     csvReader = csv.reader(csvDataFile)
#     for row in csvReader:
#         count = count + 1
        
#         if (count%2) == 1 :
#             utf = unicode(row[0], "utf-8")
#             allstr = allstr + utf
#             arr.append(utf)
#         else:
#             st = row[0].strip('\n')
#             st = st.strip('\r')
#             st = st.strip('\n')
#             labels.append(st)
count = 0
with open('vnxhtrain.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        count = count + 1
        
        if (count%2) == 1 :
            utf = unicode(row[0], "utf-8")
            allstr = allstr + utf
            arr.append(utf)
        else:
            st = row[0].strip('\n')
            st = st.strip('\r')
            st = st.strip('\n')
            labels.append(st)

# Create diction
allstr = allstr.replace("," , "").replace("." , "")
allstr = ViTokenizer.tokenize(allstr)
allstr = allstr.lower()
diction = allstr.split()
diction = list(set(diction))
print(len(diction))
count = 0

with open('topword.txt') as f:
    content = f.readlines()

# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
print(len(content))

for i in range(len(content)):
    word = unicode(content[i], "utf-8")
    if word in diction:
        count = count + 1
        diction.remove(word)
print(count)
print(len(diction))

# Write diction to file
write(diction, "diction.file")
diction = read("diction.file")

print(len(diction))

data = []

# Predict
pre = pre.replace("," , "").replace("." , "")
pre = ViTokenizer.tokenize(pre)
pre = pre.lower()
arrpre = pre.split()
apre = makeMatrix(arrpre, diction)
dpre = np.array([apre])

for i in range(len(arr)):
    arr[i] = ViTokenizer.tokenize(arr[i])
    arr[i] = arr[i].lower()
    data.append(arr[i].replace("," , "").replace("." , "").split())

# print(repr(data).decode("unicode-escape"))

d = []
for i in range(len(arr)):
    d.append(makeMatrix(data[i],diction))

# f = open('train_data.txt', 'w')
# simplejson.dump(d, f)
# f.close()

# fl = open('label.txt', 'w')
# simplejson.dump(labels, fl)
# fl.close()

traindata = np.array(d)
label = np.array(labels)




write(label, "labels.file")
lb = read("labels.file")
write(traindata, "trains.file")
trd = read("trains.file")

# text_file = open("label.txt", "r")
# lines = text_file.read().split(',')

# text_file = open("train_data.txt", "r")
# line = text_file.read().split(',')


print("Train done")

## call MultinomialNB
clf = MultinomialNB()
# training 
clf.fit(trd, lb)

# test
print(repr(pre).decode("unicode-escape"))
print('Predicting class of dpre:', str(clf.predict(dpre)[0]), clf.predict_proba(dpre))