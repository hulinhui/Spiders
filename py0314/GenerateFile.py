# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         GenerateFile
# Description:  使用特定大小的文本生成指定大小文件
# Author:       hlh
# Date:      2023/6/13 23:39
# -------------------------------------------------------------------------------
import os
import hashlib


def generate_file(file_path, file_size_bytes):
    text = 'This is some sample text by caituotuo.'  # 要重复的文本
    text_size_bytes = len(text.encode('utf-8'))  # 每个重复文本的大小（字节单位）

    repetitions = file_size_bytes // text_size_bytes  # 需要重复的次数
    remainder = file_size_bytes % text_size_bytes  # 剩余的字节数

    with open(file_path, 'w', encoding='utf-8') as f:
        for _ in range(repetitions):
            f.write(text)
        if remainder > 0:
            f.write(text[:remainder])


def generate_random_file(file_path, file_size):
    with open(file_path, 'wb') as f:
        f.write(os.urandom(file_size))


if __name__ == '__main__':
    # 1、生成一个大小为10M的txt文件
    # generate_file('指定大小的文件.txt', 1024 * 1024 * 10)
    # 2、使用特定大小的随机数生成文件
    generate_random_file('随机生成的指定大小byte文件.txt', 1024 * 1024)
