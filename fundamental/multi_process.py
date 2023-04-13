#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
@File   :   multi_process.py
@Author :   Zhenhe Zhang
@Date   :   2023/3/24
@Notes  :   https://blog.csdn.net/weixin_41099877/article/details/107956679

@More   :   包含多进程/多线程的实现示例
"""

import time


def add(n: int) -> int:
    s = 0
    for i in range(n):
        s += 1
    print(f'process{n}: {s}')
    return s


def recurrent_test():
    # 串行实现
    list1 = [10000000, 2000000, 5000000, 30000000]
    resuls = []
    time_start = time.time()
    for n in list1:
        resuls.append(add(n))
    print(f'recurrent time cost: {time.time() - time_start}')


def multiprocess_test():
    # 多进程实现
    from multiprocessing import Pool
    pool = Pool(processes=4)

    list1 = [10000000, 2000000, 5000000, 30000000]
    results = []
    time_start = time.time()
    for n in list1:
        result = pool.apply_async(add, (n,))
        results.append(result)
    pool.close()
    pool.join()
    print(f'multi-process time cost: {time.time() - time_start}')

    for res in results:
        print(res.get())


def multithread_test():
    # 多线程实现
    from concurrent.futures import ThreadPoolExecutor
    pool = ThreadPoolExecutor(max_workers=4)
    list1 = [10000000, 2000000, 5000000, 30000000]
    time_start = time.time()
    for res in pool.map(add, list1):
        print(res)
    print(f'multi-thread time cost: {time.time() - time_start}')


if __name__ == "__main__":
    recurrent_test()        # 测耗时：串行实现
    multiprocess_test()     # 测耗时：多进程实现
    multithread_test()      # 测耗时：多线程实现
