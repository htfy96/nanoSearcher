#-*- coding:utf8 -*-
import lucene
lucene.initVM()
from webIndex import WebIndexer
import os
import codecs
from bs4 import BeautifulSoup
import jieba
import sqlite3
import string

def getTitle(s):
    soup = BeautifulSoup(s, from_encoding='utf-8')
    if soup.find('title'):
        return soup.find('title').get_text() 
    return ''

def getContent(s):
    soup = BeautifulSoup(s, from_encoding='utf-8')
    res = ''
    for i in soup.findAll('script'):
        i.decompose()
    soup = BeautifulSoup(soup.prettify())
    for i in soup.findAll('link'):
        i.decompose()
    soup = BeautifulSoup(soup.prettify())
    for i in soup.findAll('style'):
        i.decompose()
    soup = BeautifulSoup(soup.prettify())
    return soup.get_text()

if __name__=='__main__':
    crawler=WebIndexer()
    conn = sqlite3.connect('../info.db')
    c = conn.cursor()
    c.execute('select * from info where id>11214893')
    while True:
        try:
            raw = c.fetchone()
            if raw == None:
                break
            print (raw)
            crawler.add(id_ = str(raw[0]), name=string.lower(' '.join(jieba.cut(raw[1]))), price=str(raw[2]), 
                    imgurl=raw[3], author = string.lower(raw[4]), url=raw[5], category=string.lower(raw[6]), detail=string.lower(raw[7]), rawname=raw[1])
        except Exception,e:
            print(unicode(e))


