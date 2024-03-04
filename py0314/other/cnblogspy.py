# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         cnblogspy
# Description:  
# Author:       hulinhui779
# Date:      2024/2/27 16:33
# -------------------------------------------------------------------------------
import re
import time

import requests
from py0314.FormatHeaders import get_format_headers, headers_gw
from py0314.loggingmethod import get_logging
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = get_logging()
header = get_format_headers(headers_gw)


def get_response(url, method='get', data=None):
    try:
        response = requests.request(method=method, url=url, headers=header, data=data, verify=False)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response
    except Exception as e:
        logger.info(e)


def get_cnblogs_data(div):
    cnblogs_item = {'title': div.select_one('div.post_item_body > h3 > a').get_text(),
                    'titlelnk': div.select_one('div.post_item_body > h3 > a').get('href'),
                    'blogslink': div.select_one('p.post_item_summary > a').get('href'),
                    'blogsname': div.select_one('div.post_item_foot > a').get_text(),
                    'blogstime': div.select_one('div.post_item_body > div.post_item_foot').text.split()[3],
                    'blogscomment':
                        re.findall(r'(\d+)', div.select_one('div.post_item_foot > span.article_comment').get_text())[
                            0],
                    'blogsread':
                        re.findall(r'(\d+)', div.select_one('div.post_item_foot > span.article_view').get_text())[0]}
    return cnblogs_item


def get_cnblogs_detail(response):
    today_data = []
    if not response:
        logger.info('博客园列表页获取失败!')
        return today_data
    soup = BeautifulSoup(response.text, 'lxml')
    cnblogs_divs = soup.select('div#post_list > div.post_item')
    for div in cnblogs_divs:
        article_date = div.select_one('div.post_item_body > div.post_item_foot').text.split()[2]
        today_date = time.strftime('%Y-%m-%d', time.localtime())
        if today_date == article_date:
            cnblogs_data = get_cnblogs_data(div)
            today_data.append(cnblogs_data)
    return today_data


def main():
    cnblogs_python_url = 'https://www.cnblogs.com/legacy/cate/python/'
    cnblogs_resp = get_response(cnblogs_python_url)
    today_list = get_cnblogs_detail(cnblogs_resp)
    if not today_list:
        logger.info('博客园今日没有文章记录!')
        exit()
    for cnblogs_name in today_list:
        print(cnblogs_name)


if __name__ == '__main__':
    main()
