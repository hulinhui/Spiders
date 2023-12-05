# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         bz_jijian.py
# Description:  
# Author:       hlh
# Date:      2021/10/2 18:45
# 当前脚本存在请求加密及响应加密[1、处理请求加密 2、响应加密]
# -------------------------------------------------------------------------------
import hashlib
import time

import requests


def get_encry_parameter():
    timestamp = str(int(time.time() * 1000))
    access = 'application/json' + 'bz.zzzmh.cn' + '273a3b6b44a285e367af744c37eb30f6'
    captcha = hashlib.sha256(access.encode('utf8')).hexdigest()
    return captcha, timestamp


def get_html(url, access, timestamp, page=1):
    header = {
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'captcha': access,
        'cache-control': 'no-cache',
        'content-length': '30',
        'content-type': 'application/json',
        'location': 'bz.zzzmh.cn',
        'origin': 'https://bz.zzzmh.cn',
        'referer': 'https://bz.zzzmh.cn/',
        'timestamp': timestamp,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4462.2 Safari/537.36'
    }
    data = {"size": 23, "current": page, "sort": 0, "category": 0, "resolution": 1, "color": 0, "categoryId": 1}
    response = requests.post(url, headers=header, json=data)
    response.encoding = 'utf-8'
    print(response.text)


def main():
    base_url = 'https://api.zzzmh.cn/bz/v3/getData'
    captcha, timestamp = get_encry_parameter()
    get_html(base_url, captcha, timestamp)


if __name__ == '__main__':
    main()
