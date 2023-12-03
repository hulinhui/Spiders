# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         豆瓣电影
# Description:  
# Author:       hlh
# Date:      2023/6/6 23:39
# -------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import pandas as pd

ua = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 '
                  'Safari/537.36 Edg/115.0.0.0'}


def get_movie_type():
    toplist_url = 'https://movie.douban.com/chart'
    response = requests.get(url=toplist_url, headers=ua)
    selector_page = BeautifulSoup(response.text, 'lxml')
    a_seletor = selector_page.select('div.types > span > a')
    type_name = [span.text for span in a_seletor]
    type_params = [span.get('href').split('&', 1)[1] for span in a_seletor]
    type_item = {name: href for name, href in zip(type_name, type_params)}
    return type_item


def get_movie_data(item, get_link, get_rank):
    movie_url = f"https://movie.douban.com/j/chart/top_list?{item[get_link.strip()].replace(':', '%3A')}&start=0&limit={get_rank}"
    movie_response = requests.get(movie_url, headers=ua)
    movie_data = movie_response.json()
    movie_rank = [movie_list['rank'] for movie_list in movie_data]
    movie_title = [movie_list['title'] for movie_list in movie_data]
    movie_score = [movie_list['score'] for movie_list in movie_data]
    movie_type = ['、'.join(movie_list['types']) for movie_list in movie_data]
    movie_roles = ['、'.join(movie_list['actors']) for movie_list in movie_data]
    movie_weburl = [movie_list['url'] for movie_list in movie_data]
    download_data = pd.DataFrame(
        {"排名": movie_rank, "名字": movie_title, "评分": movie_score, "类型": movie_type, "演员": movie_roles,
         "链接": movie_weburl})
    download_data.to_excel("movie.xlsx", index=False)


def main():
    type_info = get_movie_type()
    get_link = input("请选择查询的类型：")
    get_rank = input("请输入查询的记录数:")
    get_movie_data(type_info, get_link, get_rank)


if __name__ == '__main__':
    main()
