# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         SunshineMovie
# Description:  爬取电影天堂首页的2023新片精品数据
# Author:       hlh
# Date:      2023/6/17 11:22
# -------------------------------------------------------------------------------
import re

import pandas as pd
import requests


def get_html(url, headers=None):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        return None


def get_reg_data(pattern, text):
    if not text:
        return None
    result = pattern.findall(text)
    if not result:
        return None
    return result


def download_data(data):
    detail_list = []
    if not data:
        print('获取首页新片精品数据失败！')
        return
    pattern_three_str = '◎译　　名(.*?)<br />◎片　　名(.*?)<br />◎年　　代(.*?)<br />◎产　　地(.*?)<br />◎类　　别(.*?)<br />◎语　　言(' \
                        '.*?)<br />◎字　　幕(.*?)<br />◎上映日期(.*?)<br />◎(.*)◎片　　长(.*?)<br />◎导　　演(.*?)<br ' \
                        '/>◎编　　剧(.*?)<br />◎(.*)<br />◎简　　介(.*)<br /><br /><br />'
    pattern_three = re.compile(pattern_three_str, re.S)
    for detail_info in data:
        detail_url = 'https://m.ygdy8.com/' + detail_info[0]
        # detail_url='https://m.ygdy8.com/html/gndy/dyzz/20230604/63785.html'
        detail_text = get_html(detail_url)
        data = get_reg_data(pattern=pattern_three, text=detail_text)[0]
        real_data = [
            _.strip('<br />').replace('\u3000', '').replace('&nbsp;', '').replace('&middot;', '·').replace('<br />',
                                                                                                           '|').replace(
                '&hellip;', '...') for
            _ in data]
        detail_list.append(real_data)
    else:
        download_data = pd.DataFrame(detail_list)
        download_data.to_excel('2023新片精品.xlsx', index=False)


def main():
    top_url = 'https://m.ygdy8.com/index.html'
    pattern_one = re.compile('2023新片精品.*?<ul>(.*?)</ul>', re.S)
    pattern_two = re.compile("]<a href='(.*?)'>(.*?)</a>", re.S)
    text = get_html(top_url)
    data = get_reg_data(pattern_two, get_reg_data(pattern_one, text)[0])
    download_data(data)


if __name__ == '__main__':
    main()
