# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         async_proxy
# Description:  
# Author:       hulinhui779
# Date:      2023/12/8 10:53
# -------------------------------------------------------------------------------
import asyncio
import json
import re
import time

import aiohttp
from py0314.FormatHeaders import get_format_headers, headers_gw

seam = asyncio.Semaphore(3)

proxies = {"http": "http://hlhadmin:admin101@120.79.140.163:8849", "https": "http://hlhadmin:admin101@120.79.140.163:8849"}


async def get_response(session, url, page):
    proxy_type = url.split(':')[0]
    async with seam:
        print(f'第{page + 1}次访问获取ip页面')
        async with session.get(url=url, headers=get_format_headers(headers_gw),
                               proxy=proxies.get(proxy_type)) as response:
            page_text = await response.text()
            pattern = re.compile(r'<dd class="fz24">(.*?)</dd>', re.S)
            group_text = pattern.search(page_text)
            if not group_text:
                return
            return group_text.group(1)


async def main():
    page_url = 'http://ip.chinaz.com/'
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        task = [asyncio.create_task(get_response(session, page_url, page)) for page in range(10)]
        result = await asyncio.gather(*task)
        print(result)


if __name__ == '__main__':
    start_time = time.perf_counter()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(f'总共耗时:{time.perf_counter() - start_time:.2f}s')
