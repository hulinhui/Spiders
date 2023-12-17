# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         mzt.py
# Description:  
# Author:       hulinhui779
# Date:      2023/12/15 11:24
# -------------------------------------------------------------------------------
import json
import os.path
import re
import time

import execjs

from py0314 import get_format_headers, headers_gw
import requests
from py0314 import read_config
from thread_template.async_biaoqing import count_time

headers = get_format_headers(headers_gw)
proxy_dict = json.loads(read_config()['AUTO_PROXY_POOL']['auto_proxy'])


def get_response(url):
    try:
        response = requests.request(method='get', url=url, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except Exception as e:
        print(e)


def get_pattern(pattern_text):
    return re.compile(pattern_text, re.S)


def run_mzt_js(filename, funcname, argname):
    with open(filename, 'r', encoding='utf-8') as f:
        js_text = f.read()
    js_obj = execjs.compile(js_text)
    return js_obj.call(funcname, *argname)


def parse_page(url, pattern_text):
    print(f'正在爬取的页面:{url}')
    response = get_response(url)
    if not response:
        return []
    pattern = get_pattern(pattern_text)
    group_list = pattern.findall(response.text)
    if not group_list:
        return []
    return group_list


def get_img_info(detail_url):
    pattern_two = r'<img .*?origin" src="(.*?)" alt="(.*?)"/>'
    pattern_three = r'[(<>/\\|:*?，)]'
    img_data = parse_page(detail_url, pattern_two)
    img_info = [(os.path.split(img_url)[0], get_pattern(pattern_three).sub('_', title))
                for img_url, title in img_data[:1]][0] if img_data else ('', '')
    return img_info


def get_detail_info(url):
    pattern_one = r'<h2.*?><a href="(.*?)">.*?</a></h2>'
    url_list = parse_page(url, pattern_one)
    id_list = [os.path.split(detail_url)[1] for detail_url in url_list[:2]] if url_list else []
    return url_list, id_list


def get_img_name(ids):
    sign_url_format = 'https://mztmzt.com/app/post/p?id={}'
    sign_response = get_response(sign_url_format.format(ids))
    sign_data = sign_response.json()['data'] if sign_response else ''
    if sign_data and ids:
        img_name_list = run_mzt_js('mzt.js', 'cropty_fun', (ids, sign_data))
        return img_name_list
    else:
        print('参数有误,无法获取图片')
        return []


def save_img(prefix_img, img_name, title):
    print(f'正在下载：{title}-{img_name}')
    img_url = prefix_img + '/' + img_name
    folder_path = r'C:\Users\hulinhui779\OneDrive\Pictures\fabiaoqing\\' + title
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    file_path = folder_path + '/' + img_name
    with open(file_path, 'wb') as fp:
        img_response = get_response(img_url)
        if img_response:
            fp.write(img_response.content)
            time.sleep(1)
        else:
            print(f'图片-{img_name}:获取失败！')


@count_time
def main():
    url = 'https://mztmzt.com/photo/page/3/'
    url_list, id_list = get_detail_info(url)
    if not (url_list and id_list):
        print('列表页获取数据失败！')
        return
    for url, ids in zip(url_list, id_list):
        prefix_img, title = get_img_info(url)
        img_name_list = get_img_name(ids)
        if not (img_name_list and prefix_img and img_name_list):
            break
        global headers
        headers.update({'Referer': 'https://mztmzt.com/'})
        for img_name in img_name_list:
            save_img(prefix_img, img_name, title)
            time.sleep(0.5)
        del headers['Referer']
    print('mzt爬取完毕！')


if __name__ == '__main__':
    main()
