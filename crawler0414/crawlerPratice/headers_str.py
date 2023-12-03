# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         headers_str
# Description:  
# Author:       hlh
# Date:      2023/6/18 1:21
# -------------------------------------------------------------------------------


from lxpy import copy_headers_dict

headers_one = '''
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cache-Control: no-cache
Connection: keep-alive
Content-Length: 256
Content-Type: application/x-www-form-urlencoded
Cookie: OUTFOX_SEARCH_USER_ID="-1042076330@10.108.160.17"; OUTFOX_SEARCH_USER_ID_NCOO=443236806.0539839
Host: dict.youdao.com
Origin: https://fanyi.youdao.com
Pragma: no-cache
Referer: https://fanyi.youdao.com/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0
sec-ch-ua: "Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
'''





def get_format_headers(text):
    format_headers = copy_headers_dict(text)
    return format_headers


if __name__ == '__main__':
    pass
