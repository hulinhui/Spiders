# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         卡萨帝.py
# Description:  卡萨帝签到及抽奖小程序[export ksd=" Authorization#openId " 多账号用@分割]
# Author:       hlh
# Date:      2023/6/25 10:39
# -------------------------------------------------------------------------------
import requests
from py0314.FormatHeaders import get_format_headers
import warnings

warnings.filterwarnings('ignore')

ksd_headers = '''
Host: yx.jsh.com
Connection: keep-alive
Content-Length: 113
Accept: application/json, text/plain, */*
Authorization: {}
MK-U-App-Code: gUsb9sx0eXEdMuc
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat
MK-Source-Code: casarte
Content-Type: application/json;charset=UTF-8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Accept-Encoding: gzip, deflate, br
Accept-Language: en-us,en
'''

ksd_data = '348f3cdf91b34a11ba76b36e3a2259a5#opKPE5c1xlLUHqRH5t-MmcC8S2ik@a61c6ef3463343af9b1e28a4b3ab1101#opKPE5U0smz4KCbQdcUya0MMYj5M'


def get_response(sign_url, headers, method='get', data=None, params=None):
    try:
        response = requests.request(method=method, url=sign_url, headers=headers, json=data, params=params,
                                    verify=False)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except Exception as e:
        print(e)


def ksd_client_sign(headers, openid, index):
    ksd_sign_url = 'https://yx.jsh.com/customer/api/user/playingMethod/game/saveClockInInfoByUserId'

    ksd_data_dict = {"playId": "20", "employeeId": "", "mobile": "", "openId": openid,
                     "parentUserId": "", "userId": ""}
    response = get_response(ksd_sign_url, headers, 'post', ksd_data_dict)
    json_data = response.json() if response else None
    sign_text = f"卡萨帝账户{index}签到结果:{json_data['message']}！" if json_data and 'code' in json_data \
        else f"卡萨帝账户{index}签到失败！ "
    print(sign_text)


def get_header_openid(text):
    token, openid = text.split('#')
    ksd_headers_dict = get_format_headers(ksd_headers.format(token))
    return ksd_headers_dict, openid


def ksd_client_luckdraw(headers, index):
    luckdraw_url = 'https://yx.jsh.com/customer/api/user/client/luckDraw'
    ksd_draw_data = {"gameId": "174464962928279552"}
    response = get_response(luckdraw_url, headers, 'post', ksd_draw_data)
    json_data = response.json() if response else None
    draw_text = f"卡萨帝账户{index}抽奖结果:{json_data['data']['prizeName']}！" if json_data and 'code' in json_data and json_data.get(
        'code') == 200 else f"卡萨帝账户{index}抽奖结果:{json_data['message']}！"
    print(draw_text)


def ksd_give_chance(headers, index):
    chance_url = 'https://yx.jsh.com/customer/api/give/chance/byLogin'
    ksd_chance_data = {"gameId": "174464962928279552"}
    response = get_response(chance_url, headers, 'post', ksd_chance_data)
    json_data = response.json() if response else None
    chance_text = f"卡萨帝账户{index}获取抽奖机会结果:{json_data['message']}！" if json_data and 'message' in json_data \
        else f"卡萨帝账户{index}获取抽奖机会失败!"
    print(chance_text)


def main():
    for index, token_and_openid in enumerate(ksd_data.split('@'), 1):
        ksd_params = get_header_openid(token_and_openid)
        ksd_client_sign(*ksd_params, index)
        ksd_give_chance(ksd_params[0], index)
        ksd_client_luckdraw(ksd_params[0], index)


if __name__ == '__main__':
    main()
