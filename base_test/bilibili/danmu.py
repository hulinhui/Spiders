# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         danmo
# Description:  
# Author:       hlh
# Date:      2021/1/25 23:21
# -------------------------------------------------------------------------------
import re

import imageio
import jieba
import requests
import wordcloud


def get_response(url):
    headers = {
        'cookie': "rpdid=|(RllR)klm~0J'ulmJRJYlR); LIVE_BUVID=AUTO5015949072445733; CURRENT_QUALITY=80; _uuid=A0ECF0E4-2F5F-6AAC-34A2-0D95199B253983850infoc; buvid3=81910F6F-8B57-4F96-95E7-90ABD694CBD7138373infoc; blackside_state=1; CURRENT_FNVAL=80; sid=jma90skk; DedeUserID=368426889; DedeUserID__ckMd5=efa4bf9409d545bd; SESSDATA=9f6ce21f%2C1624711920%2C29bfc*c1; bili_jct=5da870cd2eccb25d05d3ba2ffce6969f; bp_t_offset_368426889=475290602926330600;bfe_id=018fcd81e698bbc7e0648e86bdc49e09",
        'origin': 'https://www.bilibili.com',
        'referer': 'https://www.bilibili.com/video/BV19E41197Kc',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return response


def get_data(url):
    response = get_response(url)
    if response:
        json_data = response.json()
        if json_data['code'] == 0 and json_data['data']:
            return json_data['data']
        else:
            return None
    else:
        return None


def save_text(data_list):
    with open('bilibili弹幕.txt', 'a', encoding='utf-8') as f:
        for data in data_list:
            f.write(data + '\n')


def get_word_cloud():
    # 设置词云
    cloud_pic = imageio.imread('./20210125185743167.png')
    wc = wordcloud.WordCloud(width=1000, height=700, background_color='white',
                             font_path='msyh.ttc', scale=15, mask=cloud_pic,
                             stopwords={'哈', '哈哈', '哈哈哈哈哈'})
    with open('bilibili弹幕.txt', encoding='utf8') as f:
        cut_string = ' '.join(jieba.lcut(f.read()))
        wc.generate(cut_string)
        wc.to_file('out.png')


def main(url):
    data_list = get_data(url)
    if data_list:
        for date in data_list:
            base_url = f'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid=284452148&date={date}'
            html_text = get_response(base_url).text
            results = re.findall('.*?([\u4E00-\u9FA5]+).*?', html_text, re.S)
            save_text(results)
        get_word_cloud()
    else:
        print('你访问的数据不存在')


if __name__ == '__main__':
    date_url = 'https://api.bilibili.com/x/v2/dm/history/index?type=1&oid=284452148&month=2021-01'
    main(date_url)
