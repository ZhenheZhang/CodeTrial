#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
@File   :   test.py
@Author :   Zhenhe Zhang
@Date   :   2023/3/18
@Notes  :
"""

import unittest
from language_detect import remove_symbols, add_delim_space, text_split

class MyTestCase(unittest.TestCase):
    def test_string_utilities(self):
        self.assertEqual('It s an interesting bet from Sinema  After all  Democrats usually don t run a candidate',
                        remove_symbols('It’s an interesting bet from Sinema. After all, Democrats usually don’t run a candidate'))
        self.assertEqual('2023 年 常 用 的 python 语 言 cck 262 和 ppk353 可 以 实 现 deep learning 中 的 NN 模 型 22 和 一 些 有 用 的 33 统 计 学 44 模 型',
                        add_delim_space('2023年常用的python语言cck 262和ppk353可以实现deep learning中的NN模型22和一些有用的33统计学44模型'))
        self.assertEqual([['2023 年 常 用 的 python 语 言 cck 262 和 ppk353 可 以 实 现 deep learning 中 的 NN 模 型 22 和 一 些 有 用 的 33 统 计 学 44 模 型']],
                        text_split(input=['2023年常用的python语言cck 262和ppk353可以实现deep learning中的NN模型22和一些有用的33统计学44模型'],
                                   max_length=512, max_segments=100))


if __name__ == '__main__':
    unittest.main()