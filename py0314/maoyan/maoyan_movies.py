# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         maoyan_movies
# Description:  
# Author:       hlh
# Date:      2020/12/7 22:10
# -------------------------------------------------------------------------------
# 第一步：找到字体文件，下载下来。
# 第二步：通过Font Creator工具读取下载好的字体文件。
# 第三步：按顺序拿到各个字符的unicode编码，并写出对应的文字列表。
# 第四步：将顺序unicode编码写成对应的unicode的类型。
# 第五步：替换掉文章中对应的unicode的类型的文字。
# --------------------------------------------------------------------------------
import re

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from fontTools.ttLib import TTFont

headers = {'User-Agent': UserAgent(verify_ssl=False).random, 'Host': 'maoyan.com',
           'Referer': 'https://maoyan.com/films?yearId=15',
           'Sec-Fetch-Dest': 'document',
           'Sec-Fetch-Mode': 'navigate',
           'Sec-Fetch-Site': 'none',
           'Sec-Fetch-User': '?1',
           'Upgrade-Insecure-Requests': '1'}

headers2 = {'User-Agent': UserAgent(verify_ssl=False).random, 'Host': 'maoyan.com',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'}

HOST = 'https://maoyan.com'
fontdict = {'uniF489': '0', 'uniE137': '8', 'uniE7A1': '9', 'uniF19B': '2', 'uniF4EF': '6',
            'uniF848': '3', 'uniE343': '1', 'uniE5E2': '4', 'uniE8CD': '5', 'uniF88A': '7', }


def get_moviescore(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        ddlist = soup.select('div.movies-list dd')
        for dd in ddlist:
            a = dd.select_one('a')
            detail_url = HOST + a.get('href')
            get_detail_html(detail_url)
    else:
        print(f'页面获取失败{url},状态码为:{response.status_code}')


def get_detail_html(url):
    response = requests.get(url, headers=headers2)
    if response.status_code == 200:
        detail_text = response.text
        movies = {}
        soup = BeautifulSoup(detail_text, 'lxml')
        data = replace_text(detail_text)  # 获取评分、票房、评价等数据
        # 获取字体文件解析[不使用，规律见fontdict]
        # font_pattern=re.compile(",[\s\S]+?url\('(.*?)'\) format\('woff'\)")
        # font_url='http:'+font_pattern.search(detail_text,re.S).group(1)
        # print(font_url)
        # get_font(font_url)

        # 电影名称
        movies['name'] = soup.select_one('div.movie-brief-container > h1').string
        # 电影英文名称
        movies['enname'] = soup.select_one('div.movie-brief-container > div ').string
        # 电影标签
        movies_tag = soup.select('div.movie-brief-container > ul > li:nth-of-type(1)> a')
        movies['movies_tag'] = [tag.text.strip() for tag in movies_tag]
        # 电影国家
        movies_country = soup.select('div.movie-brief-container > ul > li:nth-of-type(2)')[0].text
        movies['movies_country'] = movies_country.split('/')[0].strip()
        # 电影时长
        movies['movies_time'] = movies_country.split('/')[-1].strip()
        # 上映时间
        movies['datetime'] = soup.select('div.movie-brief-container > ul > li:nth-of-type(3)')[0].text
        # 猫眼口碑
        if len(data) < 3:  # 未上映电影
            movies['xiangkan'] = data[0]
            movies['box_office'] = '暂无'
        else:  # 已上映电影
            movies['score'] = data[0]  # 评分
            movies['score_num'] = data[1] + soup.select_one('span.score-num').get_text().split('万')[-1]
            movies['box_office'] = data[2] + soup.select_one('span.unit').text
        print(movies)
    else:
        print(f'详情页获取失败{url},状态码为:{response.status_code}')


def get_font(url):
    resp = requests.get(url)
    print(resp.status_code)
    with open('maoyanfont.woff', 'wb') as f:
        f.write(resp.content)
    font = TTFont('maoyanfont.woff')
    font.saveXML('maoyanfont.xml')
    font_list = font.getGlyphOrder()[2:]
    font_list2 = font.getGlyphNames()
    print(font_list, font_list2)


def replace_text(text):
    data_info = re.findall('<span class="stonefont">(.*?)</span>', text, re.S)
    datalist = []
    for data in data_info:
        data = data.replace('&#x', '').replace(';', '')
        new_data = None
        for key in fontdict:
            if new_data is None:
                new_data = data.replace(key[3:].lower(), fontdict[key])
            else:
                new_data = new_data.replace(key[3:].lower(), fontdict[key])
        datalist.append(new_data)
    return datalist


def main():
    url = 'https://maoyan.com/films?catId=3'
    get_moviescore(url)


if __name__ == '__main__':
    main()
