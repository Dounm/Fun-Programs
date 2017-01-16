# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys
import jieba
import codecs
import csv
from time import time

# load stopwords
with codecs.open('stopword.txt', 'r', 'utf-8') as f:
    stop_list = f.readlines()
stop_list = map(lambda x: x[:len(x)-1], stop_list) #do not use rstrip(), because the stopwords has some backspace
print len(stop_list)
stop_set = set(stop_list)

# seged doc
seged_path = './seged.article'
rawdata_path = sys.argv[1]
t0 = time()
fout = open(seged_path, 'w')
with open(rawdata_path, 'r') as f:
    line_list = f.readlines()
    for docid, line in enumerate(line_list):
        # remove all numbers, Englisth letters and unvisible ascii character
        line = line.rstrip().translate(None,'abcdefghijklmnopqrstuvwxyz1234567890\f\r\n\v').decode('utf-8')
        seg = jieba.cut(line)
        tlist = []
        for word in seg:
            if word not in stop_set:
                tlist.append(word)
        seged_doc = ' '.join(tlist).encode('utf-8')
        fout.write(seged_doc+'\n')
        print docid
fout.close()
print("done in %0.3fs." % (time() - t0))
