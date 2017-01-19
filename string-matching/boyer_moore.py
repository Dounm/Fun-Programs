# -*- coding:utf-8 -*-
#!/usr/bin/env python
#
#   Author  :   Dounm
#   E-mail  :   niuchong893184@gmail.com
#   Date    :   17/01/18 18:54:22
#   Desc    :   Implement the Boyer-Moore character matching algorithm


import os
import sys

def bad_character(substring):
    length = len(substring)
    bads = dict()
    # not the most efficent method
    for i, char in enumerate(substring):
        bads[char] = i
    return bads

def good_suffix(substring):
    length = len(substring)
    goods = [None] * length
    # behind records the index of starting char of the longest suffix that equals prefix til now
    behind = length 
    for i in reversed(range(length)):
        suffix = substring[i:]
        # this must be length-1, not i, because good suffix can be overlapped
        pos = substring.rfind(suffix, 0, length-1) 
        if substring.startswith(suffix):
            behind = i
        if pos != -1:
            goods[i] = i - pos
        else:
            goods[i] = behind
    return goods

def boyer_moore_match(string, substring):
    bads = bad_character(substring)
    goods = good_suffix(substring)
    
    len1 = len(string)
    len2 = len(substring)
    i = len2 - 1
    j = len2 - 1
    while i < len1 and j >= 0:
        if string[i] == substring[j]:
            i -= 1
            j -= 1
        else:
            # bad character
            if string[i] not in bads:
                bad = j + 1
            else:
                pos = bads[string[i]] 
                bad = j - pos
                if bad < 0:
                    bad = 1
            
            # good suffix
            if j == len2-1:
                good = 1
            else:
                good = goods[j+1]

            i += max(bad, good) + (len2 - 1 - j)
            j = len2 - 1

    if j == -1:
        return i + 1
    else:
        return -1

if __name__ == '__main__': 
    string = unicode(sys.argv[1])
    pat = unicode(sys.argv[2])
    print boyer_moore_match(string, pat)
