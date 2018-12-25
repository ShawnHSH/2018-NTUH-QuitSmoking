# this program extract the drug terms from medical records using DrugBank
import json
from collections import OrderedDict

import jieba
import pymysql
import os
import numpy as np
import matplotlib.pyplot as plt
import sys
import re
import jieba.posseg as pseg
jieba.load_userdict("drugbank.txt")
#failed to use mysql quering the drugbank database
# db = pymysql.connect(host="127.0.0.1",user="root",
#  	password="Root@123",db="drugbank",port=3306)
# cur = db.cursor()

def getDict(filepath):
  #read the case history file in json
  with open(filepath, 'r') as f:
    temp = json.loads(f.read())
  string = temp["text"]
  #use jieba to cut the string
  seg_list = jieba.cut(string)
  liststr = "/".join(seg_list)

  for myword in liststr.split("/"):
    # word = myword.strip()
    # sqlstr = "SELECT count(*) FROM drugbank WHERE name = '%s'",str(myword)
    # cur.execute(sqlstr)
    # result = cur.fetchone()
    # found = result[0]
    if( myword.strip() in Allterm and myword.strip() not in myList and myword.strip() not in myDict):
      myDict[myword.strip()] = 1
      myList.append(myword.strip())
    elif(myword.strip() in Allterm and myword.strip() not in myList and myword.strip() in myDict):
      myDict[myword.strip()] += 1
      myList.append(myword.strip())
  print(myDict)
  del myList[:]
  f.close()


myDict = dict()
myList = []
Allterm = []

with open('drugbank.txt','r',encoding='UTF-8') as f:
  for line in f:
    Allterm.append(line.strip('\n'))
print(Allterm)
#class_3_4目录下全是该类病人的json病历档案
path = "C:\\Users\\Harold\\Desktop\\ntuh\\RESTfulAPI.client\\Java\\drugbank\\class_3_4\\"
f_list = os.listdir(path)
for i in f_list:
   if os.path.splitext(i)[1] == '.json':
     print(path+i)
     getDict(path+i)

#sort the dictionary by value
#del myDict['Nicotine']
sorted_dict = OrderedDict(sorted(myDict.items(),key = lambda item: item[1],reverse = True))
#plot barsh diagram
plt.barh(list(sorted_dict.keys()),list(sorted_dict.values()))
plt.show()


# for denot in temp["denotations"]:
#   str_begin = denot['span']["begin"]
#   str_end = denot['span']['end']
#   str = string[str_begin:str_end]
    # context = string[str_begin-100:str_end+100]
    # print(str)
    # print(context)
