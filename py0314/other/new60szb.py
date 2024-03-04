# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         new60szb.py
# Description:  
# Author:       hulinhui779
# Date:      2024/2/27 14:11
# -------------------------------------------------------------------------------
import time

import requests
from lxml import etree
from py0314.NotifyMessage import send_ding
from py0314.loggingmethod import get_logging

title = '163早报'
logger = get_logging()  # 日志
logger.info('163早报信息如下:')


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    try:
        resp = requests.get(url=url, headers=headers)
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        return resp.text
    except Exception as e:
        logger.info(f'接口访问失败,失败原因:{e}')


def parse_html(text):
    if text:
        tree = etree.HTML(text)
        li_list = tree.xpath('//ul[@class="list-home"]/li')
        for li in li_list:
            article_date = li.xpath('./div[@class="white-post-entry"]//span[@class="splitdots"]/text()')[0]
            today_date = time.strftime('%Y-%#m-%d', time.localtime())
            if today_date == article_date.split()[0]:
                article_href = li.xpath('.//h2/a/@href')[0]
                return article_href
        else:
            logger.info('今日暂无简报信息')


def get_aeticle_info(html):
    text = '获取每日60s详情页失败！'
    if html:
        tree = etree.HTML(html)
        post_element = tree.xpath('//div[@class="card-body"]')[0]
        post_head_text = post_element.xpath('./div[1]/h1/text()')[0] + '\n'
        post_body_text = '\n'.join(post_element.xpath('./div[@class="post-content"]/div//text()')).strip()
        text = post_head_text + post_body_text
    return text


def main():
    new_text = '文章详情页获取失败！'
    home_url = 'https://www.booe.cc/'
    html = get_html(home_url)
    article_href = parse_html(html)
    if article_href:
        text = get_html(article_href)
        new_text = get_aeticle_info(text)
    logger.info(new_text)
    send_ding(title, mode=1)


if __name__ == '__main__':
    main()
