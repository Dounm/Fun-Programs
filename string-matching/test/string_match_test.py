# -*- coding:utf-8 -*-
#!/usr/bin/env python
#
#   Author  :   Dounm
#   E-mail  :   niuchong893184@gmail.com
#   Date    :   17/01/19 19:57:20
#   Desc    :   Test the string match algorithm: KMP and Boyer-Moore


import os
import sys
import unittest

sys.path.insert(0, '..')
import kmp
import boyer_moore

class TestStringMatch(unittest.TestCase):
    
    def test_1(self):
        string = 'abbadcababacab'
        substring = 'babac'
        self.assertEquals(kmp.kmp_match(string, substring), 7)
        self.assertEquals(boyer_moore.boyer_moore_match(string, substring), 7)

    def test_2(self):
        string = 'bcabcdababcabaabcbcabababacbacabeeacda'
        substring = 'bcababab'
        self.assertEquals(kmp.kmp_match(string, substring), 17)
        self.assertEquals(boyer_moore.boyer_moore_match(string, substring), 17)

    def test_3(self):
        string = 'dieiabgjkriabddioababa'
        substring = 'eigha'
        self.assertEquals(kmp.kmp_match(string, substring), -1)
        self.assertEquals(boyer_moore.boyer_moore_match(string, substring), -1)

    def test_4(self):
        string = 'a'
        substring = 'b'
        self.assertEquals(kmp.kmp_match(string, substring), -1)
        self.assertEquals(boyer_moore.boyer_moore_match(string, substring), -1)

    def test_5(self):
        string = 'a'
        substring = 'a'
        self.assertEquals(kmp.kmp_match(string, substring), 0)
        self.assertEquals(boyer_moore.boyer_moore_match(string, substring), 0)

    def test_6(self):
        string = 'aaaaaaa'
        substring = 'aaaa'
        self.assertEquals(kmp.kmp_match(string, substring), 0)
        self.assertEquals(boyer_moore.boyer_moore_match(string, substring), 0)

    def test_7(self):
        string = 'aa'
        substring = 'aaaa'
        self.assertEquals(kmp.kmp_match(string, substring), -1)
        self.assertEquals(boyer_moore.boyer_moore_match(string, substring), -1)

if __name__ == '__main__': 
    unittest.main()
