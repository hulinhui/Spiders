# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         有道翻译
# Description:  
# Author:       hlh
# Date:      2023/6/18 0:40
# -------------------------------------------------------------------------------
import hashlib
import time
from urllib.parse import quote

import requests

# headers = headers_str.get_format_headers(headers_str.headers_one)

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'dict.youdao.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0'
}


def get_sign(timestamp):
    text = f'client=fanyideskweb&mysticTime={timestamp}&product=webfanyi&key=fsdsogkndfokasodnaso'
    return hashlib.md5(text.encode()).hexdigest()


def get_tramslate_result(url, data):
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except Exception as e:
        print(e)


def youdao_translate(keyword):
    translate_url = 'https://dict.youdao.com/webtranslate'
    timestamp = int(time.time() * 1000)
    data = f'i={quote(keyword)}&from=zh-CHS&to=en&domain=0&dictResult=true&keyid=webfanyi&sign={get_sign(timestamp)}&client=fanyideskweb&product=webfanyi&appVersion=1.0.0&vendor=web&pointParam=client%2CmysticTime%2Cproduct&mysticTime={timestamp}&keyfrom=fanyi.web'
    result_response = get_tramslate_result(translate_url, data)
    print(result_response.text)


def main():
    keyword = input('请输入需要翻译的内容：')
    data = youdao_translate(keyword)


if __name__ == '__main__':
    main()
