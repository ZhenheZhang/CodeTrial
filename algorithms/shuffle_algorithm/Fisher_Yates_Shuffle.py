#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
@File   :   Fisher_Yates_Shuffle.py
@Author :   Zhenhe Zhang
@Date   :   2023/4/13
@Notes  :   https://blog.csdn.net/qq_27437781/article/details/88663477
            1. 从还没处理的数组（假如还剩k个），随机产生一个[0, k]之间的数字p（假设数组从0开始）；
            2. 从剩下的k个数中把第p个数取出
            3. 重复步骤2和3直到数字全部取完
            4. 从步骤3取出的数字序列便是一个打乱了的数列
"""

import random
from typing import List


def fisher_yates_shuffle(in_list: List[int]) -> List[int]:
    result = []
    while in_list:
        p = random.randrange(start=0, stop=len(in_list))
        result.append(in_list[p])
        in_list.pop(p)
    return result


if __name__ == "__main__":
    input_list = [1, 2, 2, 3, 3, 4, 5, 10]
    print(fisher_yates_shuffle(input_list))
