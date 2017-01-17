# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys

def get_suffix_set(string):
    length = len(string)
    suffixs = set()
    for i in range(1, length):
        suffixs.add(string[i:])
    return suffixs

def cal_next(string):
    prefixs = set()
    length = len(string)
    nexts = [None] * length
    for i in range(1, length+1):
        substring = string[0:i]
        prefixs.add(substring[:-1])
        suffixs = get_suffix_set(substring)
        intersect = prefixs & suffixs
        if intersect == set([]):
            nexts[i-1] = 0
        elif len(intersect) == 1:
            nexts[i-1] = len(list(intersect)[0])
        else:
            nexts[i-1] = reduce(lambda a,b: max(len(a),len(b)), intersect)
    return nexts

def kmp_match(string, substring):
    nexts = cal_next(substring)
    assert(len(nexts) == len(substring))

    len1 = len(string)
    len2 = len(substring)
    i = 0
    j = 0
    while i < len1:
        if string[i] == substring[j]:
            if j == len2-1:
                return i - len2 + 1
            i += 1
            j += 1
        else:
            if j == 0:
                i += 1
                continue
            j -= j - nexts[j-1]
    return -1

def match_count(string, substring):
    assert(type(string) == unicode)
    assert(type(substring) == unicode)

    res = 0
    length = len(substring)
    match_cnt = 0
    cur_string = string
    while 1:
        cur_string = cur_string[res:]
        ret = kmp_match(cur_string, substring) 
        if ret == -1:
            return match_cnt
        else:
            match_cnt += 1
        res = ret + length


if __name__ == '__main__':
    a = sys.argv[1]
    b = sys.argv[2]
    a = unicode(a)
    b = unicode(b)
    # print kmp_match(a, b)
    print match_count(a, b)
