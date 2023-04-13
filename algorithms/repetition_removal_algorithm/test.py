#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
@File   :   test.py
@Author :   Zhenhe Zhang
@Date   :   2023/3/18
@Notes  :
"""
import json
import unittest
from repetition_removal import is_repetition_detect


class MyTestCase(unittest.TestCase):
    def test_string_utilities(self):
        with open('samples_mini.jsonl', 'r', encoding='utf8') as fin:
            for line in fin.readlines():
                text = json.loads(line)["text"]
                self.assertEqual(True, is_repetition_detect(text))


if __name__ == '__main__':
    unittest.main()