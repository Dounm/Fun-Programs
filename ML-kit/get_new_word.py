# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys
import codecs
import re

sys.path.insert(0, '../string-matching/')
import kmp

pat = re.compile(u'[\u4e00-\u9fa5]+$')

chinese_deny_set = set(['在', '对', '的', '斤', '后'])

def filter_substring(substring):
    if pat.match(substring) is None:
        return False
    if substring[0].encode('utf-8') in chinese_deny_set:
        return False
    if substring[-1].encode('utf-8') in chinese_deny_set:
        return False
    return True


def get_new_words(doc, min_len, max_len, count_thresh):
    assert(type(doc) == unicode)
    
    new_words = []
    begin = 0
    length = len(doc)
    for cur_len in range(min_len, max_len):
        for begin in range(length - cur_len):
            substring = doc[begin: begin+cur_len]
            if not filter_substring(substring):
                continue

            string = doc[begin+cur_len:]
            match_cnt = kmp.match_count(string, substring)
            if match_cnt >= count_thresh:
                # judge if new word overlapping older word or the older word overlapping new word
                is_overlapped = False
                dels = []
                for j, word in enumerate(new_words):
                    if word == substring:
                        is_overlapped = True
                        break
                    if substring in word:
                        is_overlapped = True
                        break
                    if word in substring:
                        dels.append(j)
                        # del new_words[j]
                for d in sorted(dels, reverse=True):
                    del new_words[d]
                if not is_overlapped:
                    new_words.append(substring)
    
    return new_words


if __name__ == '__main__':
    path = sys.argv[1]
    min_len = int(sys.argv[2])
    max_len = int(sys.argv[3])
    count_thresh = int(sys.argv[4])

    with codecs.open(path, 'r', 'utf-8') as f:
        cnt = 0
        for line in f:
            new_words = get_new_words(line.strip(), min_len, max_len, count_thresh)
            print new_words
            for i in new_words:
                print "[" + i.encode('utf-8') + "]"

