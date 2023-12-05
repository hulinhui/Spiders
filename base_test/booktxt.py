# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         booktxt.py
# Description:  
# Author:       hlh
# Date:      2021/1/11 21:54
# -------------------------------------------------------------------------------
import os

import requests
from fake_useragent import UserAgent
from lxml import etree


class BookTxt():
    def __init__(self, name):
        self.name = name
        self.search_url = 'https://so.biqusoso.com/s1.php?ie=utf-8&siteid=booktxt.net&q={}'
        self.headers = {'User-Agent': UserAgent().random}
        self.filepath = 'D:/pycharm/PyCharm2020.2.2/projects/Spiders/base_test/'

    def get_html(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response
        except Exception as e:
            print(e)

    def get_book_url(self, html):
        if html:
            tree = etree.HTML(html.text)
            li_list = tree.xpath('//div[@class="search-list"]/ul/li')
            for li in li_list:
                book_name = li.xpath('//span[@class="s2"]/a/text()')[0]
                if book_name == self.name:
                    book_url = li.xpath('//span[@class="s2"]/a/@href')[0]
                    return book_url
                else:
                    print(f"未找到:{self.name}")
        else:
            print(f"搜索页获取失败:{html.status_code}")

    def get_detail_url(self):
        search_text = self.get_html(self.search_url.format(self.name))
        book_url = self.get_book_url(search_text)
        book_html = self.get_html(book_url)
        return book_html

    def get_chapter_url(self, book_html):
        try:
            tree = etree.HTML(book_html.text)
            dd_list = tree.xpath('//div[@id="list"]/dl/dd/a/@href')[6:]
            real_list = [book_html.url + href for href in dd_list]
            return real_list
        except Exception as e:
            print(e)

    def parse_detail(self, html):
        if html:
            tree = etree.HTML(html.text)
            chapter_name = tree.xpath('//div[@class="bookname"]/h1/text()')[0]
            content = ''.join(tree.xpath('//div[@id="content"]/text()')[:-1]).replace('\r', '\n').replace('\xa0',
                                                                                                          '').replace(
                '武动乾坤', '')
            return chapter_name, content
        else:
            print(f'详情页获取失败:{html.status_code}')

    def download_txt(self, data):
        if data:
            filepath = self.filepath + self.name + '/'
            if not os.path.exists(filepath):
                os.mkdir(filepath)
            pathname = filepath + data[0] + '.txt'
            with open(pathname, 'w', encoding='utf8') as fp:
                fp.write(data[0] + data[1])
            print(f'{data[0]}:下载完成')
        else:
            print('数据获取失败')

    def run(self):
        book_html = self.get_detail_url()
        url_list = self.get_chapter_url(book_html)
        for url in url_list:
            detail_text = self.get_html(url)
            book_info = self.parse_detail(detail_text)
            self.download_txt(book_info)
        print(f'{self.name}:下载完成')


if __name__ == '__main__':
    bookname = input("请输入要下载的book名：")
    book = BookTxt(bookname)
    book.run()
