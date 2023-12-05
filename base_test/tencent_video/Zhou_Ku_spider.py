# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         Zhou_Ku_spider.py
# Description:  
# Author:       hlh
# Date:      2022/3/14 14:20
# -------------------------------------------------------------------------------
import os
import re
from os.path import splitext, dirname, exists, basename

import requests
from bs4 import BeautifulSoup

###
first_seletor_page = 'div.turn > a:nth-of-type(2)'
second_seletor_page = 'div.turn > a:nth-of-type(2)'
detail_title_and_href_seletor = 'div#xinbizhi > a:nth-of-type(2)'
imga_html_seletor = 'div.bizhiin > a'
imga_seletor = 'img#imageview'

path = 'C:/Users/hlh/Pictures/Saved Pictures/zhuoku/'


#####


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4884.0 Safari/537.36 Edg/100.0.1181.0',
        'Referer': 'http://www.zhuoku.com/'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = 'GBK'
        return response
    except Exception as e:
        print(e)


def get_page_total(url, seletor, field, suffix):
    html = get_html(url)
    page_total = parse_html(html, flag=True, selector1=seletor)
    if isinstance(page_total, int):
        base_url = url.rsplit('.', 1)[0] if url.endswith('htm') else url
        page_list = [url if page == 1 else f'{base_url}{field}{page}.{suffix}' for page in range(1, page_total + 1)]
    else:
        page_list = [url]
    return page_list


def get_detail_html(data):
    for info in data:
        print(f'正在获取详情页:{info[0]}')
        second_page_list = get_page_total(info[1], seletor=second_seletor_page, field='_', suffix='htm')
        for second_url in second_page_list:
            prefix_url = dirname(second_url)
            html = get_html(second_url)
            img_data = parse_html(html, selector1=imga_html_seletor)
            for img_info in img_data:
                img_href = prefix_url + '/' + img_info[1]
                html = get_html(img_href)
                img_href= parse_html(html, selector1=imga_seletor, attrs_one='src', attrs_two='alt')
                if not img_href:
                    print('图片跳转有错误，跳过')
                    continue
                save_pic(img_href[0][0], info[0])
                # print(img_href)


def save_pic(url, dirname):
    replce_name = re.sub('[#$%^&*()_（）【】！\d+ /]', '', dirname[:25])
    print(replce_name)
    filename = path + replce_name + '/'
    if not exists(filename): os.makedirs(filename)
    filepath = filename + basename(url)
    with open(filepath, 'wb') as f:
        html = get_html(url)
        if html:
            f.write(html.content)
            print(f'{basename(url)}:下载成功')
        else:
            print(f'{basename(url)}:下载失败')


def parse_html(html, flag=False, selector1=None, attrs_one='title', attrs_two='href'):  # 获取页面及内容
    if html:
        soup = BeautifulSoup(html.text, 'lxml')
        if flag:
            try:
                page_href = soup.select_one(selector1).get('href')
                page_count = splitext(page_href)[0].split('_')[1]
                return int(page_count)
            except Exception as e:
                # print(e)
                return None
        else:
            try:
                a_list = soup.select(selector1)
                tuple_data = [(a.get(attrs_one), a.get(attrs_two)) for a in a_list][:1]
                return tuple_data
            except Exception as e:
                print(e)
                return []
    else:
        print('html页面获取失败')


def main():
    base_url = 'http://www.zhuoku.com/hot/'
    page_link = get_page_total(base_url, first_seletor_page, field='index_', suffix='html')
    # page_link = ['http://www.zhuoku.com/hot/']
    for link in page_link:
        print(f'正在获取页面:{link}')
        html = get_html(link)
        info_data = parse_html(html, selector1=detail_title_and_href_seletor)
        get_detail_html(info_data)


if __name__ == '__main__':
    main()
