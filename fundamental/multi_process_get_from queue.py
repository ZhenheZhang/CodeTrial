#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
@File   :   multi_process_get_from queue.py
@Author :   Zhenhe Zhang
@Date   :   2023/4/13
@Notes  :   MultiProcessing and Queue
@More   :   这是个简版“玩具”，应用示例见 https://github.com/ServiceNow/multithreaded-estimators/tree/1d0fba758d183193a822b8e44bda98a9443b456d
"""

from multiprocessing import Process, Queue


def f(q):
    q.put([42, None, 'hello'])


if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()
