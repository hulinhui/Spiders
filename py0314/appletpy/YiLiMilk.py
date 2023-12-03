# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         YiLiMilk
# Description:  # 伊利牛奶 小程序
# 抓取 https://msmarket.msx.digitalyili.com  中的access-token
# export ylnn="  access-token "
# 多账号用 换行 或 @ 分割
# 注意脚本运行以后 在登录小程序ck会失效
# Author:       hlh
# Date:      2023/6/20 17:32
# -------------------------------------------------------------------------------
import requests
from py0314.NotifyMessage import read_config
import warnings

warnings.filterwarnings('ignore')


def get_headers(token):
    return {
        'Host': 'msmarket.msx.digitalyili.com',
        'content-type': 'application/json',
        'access-token': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI '
                      'MiniProgramEnv/Windows WindowsWechat'
    }


def get_data(url, headers, method='get', data=None):
    try:
        response = requests.request(method, url, headers=headers, data=data, verify=False)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except Exception as e:
        print(e)


def get_userpoint(index, token):
    point_url = 'https://msmarket.msx.digitalyili.com/gateway/api/member/point'
    response_data = get_data(point_url, get_headers(token))
    json_data = response_data.json() if response_data else {}
    data = json_data['data'] if json_data.get('status') else -1
    message = f'账号{index}总积分：{data}' if data >= 0 else f'账号{index}获取总积分失败！'
    print(message)


def sign_user(index, token):
    sign_url = 'https://msmarket.msx.digitalyili.com/gateway/api/member/daily/sign'
    response_data = get_data(sign_url, headers=get_headers(token), method='post', data={})
    json_data = response_data.json() if response_data else {}
    if json_data.get('status'):
        sign_point = json_data['data']['dailySign'].get('bonusPoint') if json_data['data']['dailySign'] else None
        text = f'账号{index}签到成功,获得{sign_point}积分' if sign_point else f'账号{index}今天已签到过了！'
        print(text)
    else:
        print(f'账号{index}签到失败！')


def main():
    token_list = read_config()['YILI']['yili_token'].split('@')
    for index, token in enumerate(token_list, start=1):
        sign_user(index, token)
        get_userpoint(index, token)


if __name__ == '__main__':
    main()
