# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         gw.py
# Description:  
# Author:       hlh
# Date:      2023/11/7 14:41
# -------------------------------------------------------------------------------

import os
import re

import requests
from bs4 import BeautifulSoup
from py0314.FormatHeaders import headers_gw, get_format_headers
from py0314.loggingmethod import get_logging
from py0314.NotifyMessage import send_ding

headers = get_format_headers(headers_gw)
logger = get_logging()

gw_login = '975081281@qq.com'
gw_password = 'cv5LgH7H7NmV7dtp547B'


def gw_account_info():
    """环境变量中获取数据"""
    params_list = ['gw_login', 'gw_password']
    real_params = [os.environ[params] for params in params_list if params in os.environ and os.environ.get(params)]
    if len(real_params) != len(params_list):
        logger.info('gw机场缺少可执行的参数！')
        exit()
    return real_params


def get_response(session, url, method='get', data=None):
    try:
        response = session.request(method=method, url=url, headers=headers, data=data)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response
    except Exception as e:
        logger.info(e)


def check_result(response, check_login=None):
    print(response.text)
    json_data = response.json() if response else {}
    result = json_data['ret'] if json_data and 'ret' in json_data else ''
    is_login = True if result else False
    if check_login:
        return is_login
    else:
        return is_login, json_data


def parse_html(response):
    text = response.text if response else ''
    soup = BeautifulSoup(text, 'html.parser')
    nick_name = soup.select_one(
        'div.dropdown > div:nth-of-type(2) strong').get_text() if soup else ''  # 获取用户昵称
    info_list = [re.sub(r'\s+', '', i.text) for i in
                 soup.select_one('div.container > div.row').select('strong')] if soup else []  # 用户信息
    member_day = [re.sub(r'\s+', '', i.text) for i in soup.select_one('div.container > div.row').select(
        'div:nth-last-of-type(1) > p.text-dark-50') if ':' in i.text] if soup else []  # 会员天数
    if info_list and member_day:
        info_list.insert(0, nick_name)
        info_list.insert(2, member_day[0])
        return info_list
    else:
        return []


def gw_login_on(login, password):
    """gw登录信息"""
    session = requests.session()
    login_url = 'https://m.mmomm.io/auth/login'
    data = {'email': login, 'passwd': password}
    response = get_response(session, method='post', url=login_url, data=data)
    flag, data = check_result(response)
    if flag:
        logger.info(f"gw登录情况：{data['msg']}")
        return session
    else:
        logger.info(f"gw登录情况：{data['msg']}")
        logger.info('程序退出！')
        exit()


def gw_sign_in(session):
    """gw签到信息"""
    sign_url = 'https://m.mmomm.io/user/checkin'
    response = get_response(session, method='post', url=sign_url)
    flag, data = check_result(response)
    if flag:
        logger.info(f"gw签到情况：签到成功[{data['msg']}]!")
    else:
        logger.info(f"gw签到情况：签到失败[{data['msg']}]!")


def gw_userinfo(session):
    """gw用户信息"""
    user_url = 'https://m.mmomm.io/user'
    response = get_response(session, url=user_url)
    info_list = parse_html(response)
    if info_list:
        logger.info('gw用户信息：用户昵称：{},会员时长：{},{}\ngw用户信息：可用流量：{},在线设备：{},钱包余额：{}'.format(*info_list))
    else:
        logger.info(f'gw用户信息：获取用户信息数据失败!')
    gw_usersubscribe(response)


def gw_usersubscribe(response):
    """gw的订阅信息"""
    text = response.text if response else ''
    link_text = re.search(r"oneclickImport\('clash','(.*?)'\)", text)
    if link_text:
        logger.info(f'gw【clash】订阅：{link_text.group(1)}')
    else:
        logger.info('gw【clash】订阅：获取失败!')


def main():
    # login, password = gw_account_info()
    session = gw_login_on(gw_login, gw_password)
    gw_userinfo(session)
    gw_sign_in(session)
    send_ding('gw机场签到')


if __name__ == '__main__':
    main()
