# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         proxy_test
# Description:  
# Author:       hulinhui779
# Date:      2023/12/8 10:22
# -------------------------------------------------------------------------------
import re

import requests

proxies = {"http": "http://120.79.140.163:8849", "https": "http://120.79.140.163:8849"}


def get_response(url):
    try:
        response = requests.request(method='get', url=url, proxies=proxies)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except Exception as e:
        print(e)


def parse_detail_page(response):
    if not response:
        return
    text = response.text
    pattern = re.compile(r'<dd class="fz24">(.*?)</dd>', re.S)
    group_text = pattern.search(text)
    if not group_text:
        return
    return group_text.group(1)


def main():
    url = 'https://ip.chinaz.com/'
    response = get_response(url)
    ip_text = parse_detail_page(response)
    print(ip_text)


if __name__ == '__main__':
    main()
