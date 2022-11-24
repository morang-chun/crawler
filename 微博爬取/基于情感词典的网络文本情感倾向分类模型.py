# 其中，“文件5”为评论文本文档，以微博id命名方便后续对应读取。


from collections import defaultdict
import os
import re
import jieba
import codecs
def classifyWords(wordDict):
    senList = open(存储路径-情感词典).readlines()
    senDict = defaultdict()
    for s in senList:
        ls=s.split(' ',1)
        if len(ls)==2:
            senDict[ls[0]] = ls[1]
    notList = open('E:\\NOTE\\03【文本分析】\\停用词\\neg_all_dict.txt').readlines()
    degreeList = open('E:\\NOTE\\03【文本分析】\\停用词\\pos_all_dict.txt').readlines()
    degreeDict = defaultdict()
    for d in degreeList:
        ls2 = d.split(',', 1)
        if len(ls2) == 2:
            degreeDict[ls2[0]] = ls2[1]
    senWord = defaultdict()
    notWord = defaultdict()
    degreeWord = defaultdict()
    for word in wordDict.keys():
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
            senWord[wordDict[word]] = senDict[word]
        elif word in notList and word not in degreeDict.keys():
            notWord[wordDict[word]] = -1
        elif word in degreeDict.keys():
            degreeWord[wordDict[word]] = degreeDict[word]
    return senWord, notWord, degreeWord
def scoreSent(senWord, notWord, degreeWord, segResult):
    W = 1
    score = 0
    senLoc = senWord.keys()
    notLoc = notWord.keys()
    degreeLoc = degreeWord.keys()
    senloc = -1
    for i in range(0, len(segResult)):
        if i in senLoc:
            senloc += 1
            score += W * float(senWord[i])
            if senloc < len(senLoc) - 1:
                for j in range(list(senLoc)[senloc], list(senLoc)[senloc + 1]):
                    if j in notLoc:
                        W *= -1
                    if j in degreeLoc:
                        W *= float(list(degreeWord)[j])
        if senloc < len(senLoc) - 1:
            i = list(senLoc)[senloc + 1]
    return score
# uid=#微博id列表
# for n in uid:#多个微博的评论文本分别评分
txt = open('E:\PYTHON临时\评论excel\shanghaiqing.xlsx',encoding='utf8').readlines()
stop = open('E:\\NOTE\\03【文本分析】\\停用词\\百度停用词.txt').readline()
line=[]
for i in range(len(txt)):
    line.append(list(jieba.cut(txt[i])))
ScoreList=[]
for i in range(len(line)):
    words=line[i]
    num=list(range(0,len(words)))
    d=dict(zip(words,num))
    s,no,d=classifyWords(d)
    Score=scoreSent(s, no, d, words)
    ScoreList.append(Score)
VBIG=0
BIG=0
SMALL=0
VSMALL=0
MID=0
for score in ScoreList:
    if score>=3:
        VBIG=VBIG+1
    elif score>=0.5:
        BIG=BIG+1
    elif score>=-0.5:
        MID=MID+1
    elif score>-3:
        SMALL=SMALL+1
    else:
        VSMALL=VSMALL+1
print(VBIG,BIG,MID,SMALL,VSMALL)
print("---")
