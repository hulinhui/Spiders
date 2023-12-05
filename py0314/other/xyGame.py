# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         xyGame
# Description:  该脚本实现每日仙友GAME公众号消息推送
# Author:       hlh
# Date:      2023/6/10 15:20
# -------------------------------------------------------------------------------
import re
import time

import pandas
import requests

from Spiders.py0314.FormatHeaders import get_format_headers, wechat_headers
from Spiders.py0314.NotifyMessage import send_pushplus
from Spiders.py0314.loggingmethod import get_logging

headers = get_format_headers(wechat_headers)
logger = get_logging()


def get_data(url, params):
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except Exception as e:
        print(e)
        return None


def check_response_data(response, Flag):
    if not response:
        return ()
    data = response.json()
    if 'base_resp' not in data and not data.get('base_resp').get('ret'):
        return ()
    count = data['app_msg_cnt'] if Flag else None
    return data['app_msg_list'], count


def get_wechat_articles(fake_id, token, page=0, Flag=True):
    articles_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
    articles_params = {'action': 'list_ex', 'begin': page, 'count': 5, 'fakeid': fake_id, 'type': 9, 'token': token,
                       'lang': 'zh_CN', 'f': 'json', 'ajax': 1}
    response = get_data(articles_url, articles_params)
    data_tuple = check_response_data(response, Flag)
    return data_tuple


def get_day_articles(data):
    release_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[0]['create_time']))
    now_date = time.strftime('%Y-%m-%d', time.localtime(int(time.time())))
    if release_time.split()[0] == now_date:
        articles_title = data[0]['title']
        articles_link = data[0]['link']
        logger.info(f'标题：{articles_title}')
        logger.info(f'发布时间：{release_time}')
        logger.info(f'页面链接：{articles_link}')
        send_pushplus('仙友Game公众号消息推送')
    else:
        logger.info('今日还未发布公众号文章哦！')


def get_all_artocles(fake_id, token, tupele_data):
    all_list = []
    first_page_data, count = tupele_data
    page_total = int(count / 5) + 1
    for page in range(2, 4):
        if page == 2:
            page_data = first_page_data + get_wechat_articles(fake_id, token, (page - 1) * 5, Flag=False)[0]
        else:
            page_data = get_wechat_articles(fake_id, token, (page - 1) * 5, Flag=False)[0]
        data = [[item['aid'], item['title'], item['link']] for item in page_data]
        all_list.extend(data)
        time.sleep(2)
    downloads_data = pandas.DataFrame(all_list, columns=['文章id', '文章标题', '文章链接'])
    downloads_data.to_excel('仙友Game公众号文章.xlsx')


def get_check_response(keyword, response):
    if not response:
        return None
    data = response.json()
    if 'base_resp' not in data and not data.get('base_resp').get('ret'):
        return None
    return [item['fakeid'] for item in data['list'] if item['nickname'] == keyword][0]


def get_fakeId(keyword, token):
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
    search_params = {'action': 'search_biz', 'begin': 0, 'count': 5, 'query': keyword, 'token': token,
                     'lang': 'zh_CN', 'f': 'json', 'ajax': 1}
    response = get_data(search_url, params=search_params)
    fake_id = get_check_response(keyword, response)
    return fake_id


def main():
    token = re.search('token=(\d+)&', headers['Referer']).group(1)
    fake_id = get_fakeId('仙友Game', token)
    if token and fake_id:
        data_tuple = get_wechat_articles(fake_id, token)
        if data_tuple:
            get_day_articles(data_tuple[0])  # 获取每日公众号文章
            get_all_artocles(fake_id, token, data_tuple)  # 获取所有文章
        else:
            print('获取公众号文章数据失败！')
    else:
        print('获取token及fakeid值失败！')


if __name__ == '__main__':
    main()
