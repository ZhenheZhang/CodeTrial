#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
@File   :   multi_process_read_file.py
@Author :   Zhenhe Zhang
@Date   :   2023/3/24
@Notes  :   https://blog.csdn.net/Changxing_J/article/details/129707507
@More   :   干货！可直接用，多进程/线程读取文本内容
"""

import os
import sys
import time
from typing import List
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from functools import partial


def read(path: str, time_stamp: List[int]) -> List[str]:
    """
    Args:
        :param path: str 文件路径
        :param time_stamp:
        start : int 本分块的开始位置
        end   : int 本分快的结束位置
    Returns:
        content: List[str]  从文件读取的文本内容
    """

    start = time_stamp[0]
    end = time_stamp[1]
    content = []
    with open(path, 'r', encoding='utf8') as fin:
        fin.seek(start)
        if start != 0:
            while True:
                try:
                    fin.readline()
                    break
                except UnicodeDecodeError:
                    fin.seek(start + 1)
        while fin.tell() <= end:
            content.append(fin.readline())
    return content


def read_multi_process_async(path: str, n_process: int) -> List[List[str]]:
    """
    Args:
        path     : str 文件路径
        n_process : int 线程数量
    Returns:
        content: List[List[str]] 从文件读取的文本内容
    """

    size = os.path.getsize(path)
    pool = multiprocessing.Pool(processes=n_process)

    results = []
    for i in range(n_process):
        start = size // n_process * i
        end = size // n_process * (i + 1)
        result = pool.apply_async(read, (path, [start, end], ))
        results.append(result)
    pool.close()
    pool.join()

    output = []
    for res in results:
        output.append(res.get())
    return output


def read_multi_process(path: str, n_process: int) -> List[List[str]]:
    """
    Args:
        path     : str 文件路径
        n_process : int 线程数量
    Returns:
        content: List[List[str]] 从文件读取的文本内容
    """

    size = os.path.getsize(path)
    pool = multiprocessing.Pool(processes=n_process)

    results = []
    time_stamps = []
    for i in range(n_process):
        start = size // n_process * i
        end = size // n_process * (i + 1)
        time_stamps.append([start, end])

    for result in pool.map(partial(read, path), time_stamps):
        results.append(result)
    return results


def read_multi_thread(path: str, n_thread: int) -> List[List[str]]:
    """
    Args:
        path     : str 文件路径
        n_thread : int 线程数量
    Returns:
        content: List[List[str]] 从文件读取的文本内容
    """

    size = os.path.getsize(path)
    pool = ThreadPoolExecutor(max_workers=4)

    results = []
    time_stamps = []
    for i in range(n_thread):
        start = size // n_thread * i
        end = size // n_thread * (i + 1)
        time_stamps.append([start, end])

    for result in pool.map(partial(read, path), time_stamps):
        results.append(result)
    return results


def recurrent_test(path: str):
    # 串行实现
    time_start = time.time()
    content = []
    with open(path, 'r', encoding='utf8') as fin:
        for line in fin.readlines():
            content.append(line)
    print('content len={}'.format(len(content)))
    print(f'recurrent time cost: {time.time() - time_start}')


def multiprocess_async_test(path: str):
    # 多进程同步实现
    time_start = time.time()
    content_list = read_multi_process_async(path=path, n_process=4)
    print('content list len={}'.format(len(content_list)))
    for i, content in enumerate(content_list):
        print('content[{}] len={}'.format(i, len(content)))
    print(f'multiprocess Async time cost: {time.time() - time_start}')


def multiprocess_test(path: str):
    # 多进程异步实现
    time_start = time.time()
    content_list = read_multi_process(path=path, n_process=4)
    print('content list len={}'.format(len(content_list)))
    for i, content in enumerate(content_list):
        print('content[{}] len={}'.format(i, len(content)))
    print(f'multiprocess time cost: {time.time() - time_start}')


def multithread_test(path: str):
    # 多线程实现
    time_start = time.time()
    content_list = read_multi_thread(path=path, n_thread=4)
    print('content list len={}'.format(len(content_list)))
    for i, content in enumerate(content_list):
        print('content[{}] len={}'.format(i, len(content)))
    print(f'multithread time cost: {time.time() - time_start}')


if __name__ == "__main__":
    recurrent_test(path='../data/librispeech-lexicon.txt')              # 测耗时：串行实现
    multiprocess_async_test(path='../data/librispeech-lexicon.txt')     # 测耗时：多进程同步实现
    multiprocess_test(path='../data/librispeech-lexicon.txt')           # 测耗时：多进程异步实现
    multithread_test(path='../data/librispeech-lexicon.txt')            # 测耗时：多线程实现
