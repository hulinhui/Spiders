# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         FormatHeaders
# Description:  
# Author:       hlh
# Date:      2023/5/21 9:51
# -------------------------------------------------------------------------------
from lxpy import copy_headers_dict

headers = '''
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
appsource: PC
Connection: keep-alive
Content-Type: application/json;charset=UTF-8
Host: distribution.gotokeep.com
Referer: https://distribution.gotokeep.com/mgr
sec-ch-ua: "Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42
yunshl_token: eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI4ODU2NzQ2ODAyMjE1NjgzODIyMDU1NjY0ODA1MTcxMSIsImlhdCI6MTY4NDkyNDU4NywiZXhwIjoxNjg1NTI5Mzg3LCJyZWZyZXNoX3Rva2VuIjoiODg1Njc0NjgwMjIxNTY4MzgyMjA1NTY2NDgwNTE3MTEiLCJzY29wZSI6IkFDQ0VTUyIsInN0YXJ0VGltZSI6MTY4NDkyNDU4Nzk5MSwiZXhwaXJlc19pbiI6NjA0ODAwLCJ0b2tlbl90eXBlIjoiUEMiLCJsb2dpbiI6ImtlZXAxMjMiLCJpZCI6MTYzOTQ1fQ.I15shLzhceLpND0ZXcsWUNzBN9zlZVel948bMq4uIRYsZeACoPLpOOYOKX7RxxU2g6BVSr1CgmdJJC1HxUxscQ
'''


def get_format_headers():
    format_headers=copy_headers_dict(headers)
    return format_headers

if __name__ == '__main__':
    get_format_headers()
