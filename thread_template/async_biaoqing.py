# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         async_biaoqing
# Description:  
# Author:       hulinhui779
# Date:      2023/12/14 22:38
# -------------------------------------------------------------------------------
import asyncio
import json
import time
import re
import aiofiles
import aiohttp
from py0314 import get_format_headers, headers_gw
from py0314 import read_config
import os

headers = get_format_headers(headers_gw).update({'Referer': 'https://fabiaoqing.com/'})
seam = asyncio.Semaphore(5)
base_path = r'C:\Users\hulinhui779\OneDrive\Pictures\fabiaoqing\\'
proxy_str = json.loads(read_config()['AUTO_PROXY_POOL']['auto_proxy']).get('http')


async def get_html(session, url):
    async with seam:
        try:
            async with session.get(url, headers=headers) as resp:
                resp.raise_for_status()
                bin_text = await resp.read()
                return bin_text
        except Exception as e:
            print(e)


async def download_img(session, url, title):
    title = re.sub(r'[(<>/\\|:*?)]', '_', title)[:5] + os.path.splitext(url)[1]
    try:
        async with aiofiles.open(base_path + title, 'wb') as fp:
            content = await get_html(session, url)
            await fp.write(content)
            print(f'{title}:图片下载成功！')
    except Exception as e:
        print(e)


async def fetch_data(session, url, page):
    print(f'正在爬取第{page}页数据')
    content = await get_html(session, url)
    pattern = re.compile(r'data-original="(.*?)".title="(.*?)"', re.S)
    img_list = pattern.findall(content.decode())
    for img_info in img_list:
        await download_img(session, *img_info)


async def run():
    base_url = 'https://fabiaoqing.com/biaoqing/lists/page/{}.html'
    url_list = [base_url.format(page) for page in range(1, 3)]
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
    tasks = [fetch_data(session, url, page) for page, url in enumerate(url_list, 1)]
    await asyncio.gather(*tasks)
    await session.close()


def count_time(func1):
    def wrapper():
        start_time = time.perf_counter()
        func1()
        end_time = time.perf_counter()
        print(f'运行程序总耗时:{end_time - start_time:2f}s')

    return wrapper


@count_time
def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


if __name__ == '__main__':
    main()
