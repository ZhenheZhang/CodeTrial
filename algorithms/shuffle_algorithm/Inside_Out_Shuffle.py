#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
@File   :   Inside_Out_Shuffle.py.py
@Author :   Zhenhe Zhang
@Date   :   2023/4/13
@Notes  :   https://blog.csdn.net/qq_27437781/article/details/88663477
            Knuth-Durstenfeld Shuffle 是一个in-place算法，原始数据被直接打乱，
            但有些应用中可能需要保留原始数据，因此需要开辟一个新数组来存储打乱后的序列。
            Inside-Out Shuffle 算法的基本思想是设一游标i从前向后扫描原始数据的拷贝，
            在[0, i]之间随机一个下标j，然后用位置j的元素替换掉位置i的数字，再用原始数据位置i的元素替换掉拷贝数据位置j的元素。
            其作用相当于在拷贝数据中交换i与j位置处的值。

"""

import random
from typing import List


def inside_out_shuffle(in_list: List[int]) -> List[int]:
    result = in_list[:]
    for i in range(1, len(in_list)):
        j = random.randrange(start=0, stop=i)
        result[i] = result[j]
        result[j] = in_list[i]
    return result


if __name__ == "__main__":
    input_list = [1, 2, 2, 3, 3, 4, 5, 10]
    print(inside_out_shuffle(input_list))
