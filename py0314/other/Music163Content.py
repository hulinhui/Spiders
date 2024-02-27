# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         163music热评
# Description:
# Author:       hulinhui779
# Date:      2024/02/27 10:35
# -------------------------------------------------------------------------------

import asyncio
import time
import aiohttp
from py0314 import get_format_headers, headers_gw
import random

seam = asyncio.Semaphore(3)


def get_163_content(json_data):
    message_text = ''
    result = json_data['code'] if json_data and 'code' in json_data else ''
    data = json_data['data'] if result in [1, 200] else {}
    if not data:
        message_text += f"【网易云时间】：获取热评失败！"
    elif not ('name' in data and 'content' in data):
        data['name'] = data.get('songName')
        data['content'] = data.get('hotContent')
    message_text += f"【网易云时间】：{data['content']}  by--{data['name']}"
    return message_text


async def get_163_response(session, url, page):
    async with seam:
        # print(f'第{page}个api接口发起请求！')
        try:
            async with session.get(url=url, headers=get_format_headers(headers_gw)) as response:
                json_data = await response.json(content_type=False)
                return get_163_content(json_data)
        except Exception as e:
            print(e)
            return None


async def music_163_second():
    api_url_list = ['https://api.dzzui.com/api/wyypl', 'https://api.03c3.cn/api/neteaseCloud',
                    'http://api.xtaoa.com/api/wyy_comments.php', 'https://cloud.qqshabi.cn/api/comments/api.php']
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        task = [asyncio.create_task(get_163_response(session, api_url, index)) for index, api_url in
                enumerate(api_url_list, 1)]
        result = await asyncio.gather(*task)
        text = random.choice(result)
        return text


def music_163_main():
    start_time = time.perf_counter()
    loop = asyncio.get_event_loop()
    loop_task = loop.create_task(music_163_second())
    loop.run_until_complete(loop_task)
    # print(f'总共耗时:{time.perf_counter() - start_time:.2f}s')
    return loop_task.result()


if __name__ == '__main__':
    print(music_163_main())
