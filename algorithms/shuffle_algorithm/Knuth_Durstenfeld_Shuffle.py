#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
@File   :   Knuth_Durstenfeld_Shuffle.py
@Author :   Zhenhe Zhang
@Date   :   2023/4/13
@Notes  :   https://blog.csdn.net/qq_27437781/article/details/88663477
            Knuth 和 Durstenfeld 在 Fisher等人的基础上对算法进行了改进。
            每次从未处理的数据中随机取出一个数字，然后把该数字放在数组的尾部，
            即数组尾部存放的是已经处理过的数字。
            这是一个原地打乱顺序的算法，算法时间复杂度也从Fisher算法的O(n2)提升到了O(n)

@More   :   重点推荐此算法 !!!
            python random模块shuffle方法就是用Knuth Durstenfeld Shuffle方法

"""

import random
from typing import List


def knuth_durstenfeld_shuffle(in_list: List[int]) -> List[int]:
    for i in range(len(in_list) - 1, 0, -1):
        p = random.randrange(start=0, stop=i+1)
        in_list[i], in_list[p] = in_list[p], in_list[i]
    return in_list


if __name__ == "__main__":
    input_list = [1, 2, 2, 3, 3, 4, 5, 10]
    print(knuth_durstenfeld_shuffle(input_list))
