# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         async_linux_bizhi
# Description:  
# Author:       hulinhui779
# Date:      2023/12/11 21:47
# -------------------------------------------------------------------------------
import asyncio
import time
from Spiders import get_format_headers, headers_gw
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os
import aiofiles

import aiohttp
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Async_Linxu:
    def __init__(self):
        self.seam = asyncio.Semaphore(3)
        self.headers = get_format_headers(headers_gw)
        self.proxy_dict = {"http": "http://120.79.140.163:8849", "https": "http://120.79.140.163:8849"}
        self.base_url = 'https://www.linuxidc.com/Linuxwallpaper/index{}.htm'
        self.domain = 'https://www.linuxidc.com'
        self.proxy_str = self.proxy_dict.get(urlparse(self.base_url).scheme)
        self.base_path = r'C:\Users\hulinhui779\OneDrive\Pictures\pictures\\'

    async def get_html(self, session, url, down_flag=False):
        async with self.seam:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if down_flag:
                        return await response.read()
                    else:
                        return BeautifulSoup(await response.text(), 'lxml')
            except Exception as e:
                print(e)

    def parse_html(self, soup_list):
        href_list = [self.domain + link.get('href').split('..')[-1] for soup in soup_list for link in
                     soup.select('#dlNews > tr > td > a')]
        return href_list

    def parse_detail_html(self, soup_list):
        data_list = [soup.select('div#content > p > img') for soup in soup_list]
        img_list = [data['src'] for _ in data_list for data in _ if data and data.get('src')]
        real_img_list = [(self.domain + _.split('..')[-1],
                          os.path.split(_)[1]) for _ in img_list if _.startswith('..')]
        return real_img_list

    async def download_img(self, session, url, title):
        file_path = self.base_path + title
        try:
            async with aiofiles.open(file_path, 'wb') as fp:
                content = await self.get_html(session, url, down_flag=True)
                await fp.write(content)
                print(f'{title}:图片下载成功！')
        except Exception as e:
            print(e)

    async def main(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, limit=60),
                                         trust_env=True) as session:
            url_list = [self.base_url.format(f'p{i}') if i != 1 else self.base_url.format('') for i in range(1, 2)]
            task1 = [self.get_html(session, url) for url in url_list]
            soup_page_list = await asyncio.gather(*task1)
            href_list = self.parse_html(soup_page_list)
            task2 = [self.get_html(session, href) for href in href_list]
            soup_detail_list = await asyncio.gather(*task2)
            img_url_list = self.parse_detail_html(soup_detail_list)
            task3 = [self.download_img(session, *img_info) for img_info in img_url_list]
            await asyncio.gather(*task3)

    def run(self):
        start_time = time.perf_counter()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main())
        print(f'总共耗时:{time.perf_counter() - start_time:2f}s')


if __name__ == '__main__':
    al = Async_Linxu()
    al.run()
