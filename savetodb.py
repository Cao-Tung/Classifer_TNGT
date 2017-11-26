# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pymongo import MongoClient
import csv
import datetime

def get_date(text):
	res = None
	text_split = text.split(" ")
	for i in range(len(text_split)):
		if (text_split[i].find("/") != -1):
			res = text_split[i].split("/")
			break
	return res


def normalize(text):
	illegal = ["\t", "\n"]
	for char in illegal:
		text = text.replace(char, " ")
	return text


client = MongoClient()
db = client['project3']
collection = db.posts

f = open('resultdata.csv', 'r')
reader = csv.reader(f)
next(reader)

for row in reader:
	document = {'title' : None, 
			'content' : None, 
			'dead' : None, 
			'injured' : None, 
			'time' : None, 
			'comments' : [], 
			'place' : {
				'raw' : None, 
				'city' : None, 
				'latLng' : {
					'lat' : None, 
					'lng' : None
							}
						},
			'__v' : 0,
			'vehicles' : [],
			'description' : None,
			'publish' : None,
			'level' : None
	}

	document["content"] = normalize(unicode(row[0], "utf-8"))
	document["title"] = normalize(unicode(row[1], "utf-8"))
	document["description"] = normalize(unicode(row[2], "utf-8"))
	date_split = get_date(normalize(unicode(row[3], "utf-8")))
	# if (date_split != None):
	# 	document["publish"] = datetime.datetime(int(date_split[2]), int(date_split[1]), int(date_split[0]))
	# else:
	# 	print(unicode(row[3], "utf-8")[1:-1])
	# 	continue
	document["level"] = 0
	collection.insert_one(document)
f.close()
