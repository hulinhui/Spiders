# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         danmu.py
# Description:  
# Author:       hlh
# Date:      2021/1/26 23:39
# -------------------------------------------------------------------------------
import json

import imageio
import jieba
import re
import requests
import wordcloud
from fake_useragent import UserAgent

headers = {'User-Agent': UserAgent().random}


def get_response(timestamp):
    first_url = 'https://mfm.video.qq.com/danmu?'
    params = {'otype': 'json',
              'callback': 'jQuery191041901675273781214_1611678919270',
              'target_id': '6416481842&vid=t0035rsjty9',
              'session_key': '57741,0,1611680267',
              'timestamp': timestamp}
    try:
        response = requests.get(first_url, params=params, headers=headers)
        response.raise_for_status()
        # response.encoding=response.apparent_encoding
        return response
    except Exception as e:
        print(e)


def get_data(html):
    if html:
        data = re.findall('jQuery191041901675273781214_1611678919270\((.*)\)', html.text, re.S)[0]
        json_data = json.loads(data)
        if json_data['err_code'] == 0 and 'comments' in json_data:
            return json_data['comments']
        else:
            print('数据获取失败')
    else:
        print(html)


def save_txt(data):
    with open('欢乐喜剧人弹幕.txt', 'a', encoding='utf8') as fp:
        for i in data:
            fp.write(i['content'])
            fp.write('\n')


def get_word_cloud():
    # 设置词云
    cloud_pic = imageio.imread('./123.png')
    wc = wordcloud.WordCloud(width=1000, height=700, background_color='white',
                             font_path='msyh.ttc', scale=15, mask=cloud_pic)
    with open('欢乐喜剧人弹幕.txt', encoding='utf8') as f:
        cut_string = ' '.join(jieba.lcut(f.read()))
        wc.generate(cut_string)
        wc.to_file('out.png')


def main():
    timestamp = 0
    while True:
        response = get_response(timestamp)
        data = get_data(response)
        if not data:
            print('数据爬取完毕')
            break
        else:
            save_txt(data)
        timestamp += 30
    get_word_cloud()


if __name__ == '__main__':
    main()
