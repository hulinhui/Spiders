# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         ikuuu.py
# Description:
# Author:       hlh
# Date:      2023/11/6 16:38
# -------------------------------------------------------------------------------

import os
import re

import requests
from bs4 import BeautifulSoup
from py0314.FormatHeaders import headers_ikuuu, get_format_headers
from py0314.loggingmethod import get_logging
from py0314.NotifyMessage import send_ding

headers = get_format_headers(headers_ikuuu)
logger = get_logging()

iku_login = 'linhuihu9@gmail.com'
iku_password = 'HhxFBoR424L2hdpbspM4'


def xk_account_info():
    """环境变量中获取数据"""
    params_list = ['iku_login', 'iku_password']
    real_params = [os.environ[params] for params in params_list if params in os.environ and os.environ.get(params)]
    if len(real_params) != len(params_list):
        logger.info('ikuu机场缺少可执行的参数！')
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
    nick_name = soup.select_one('li.dropdown > a > div').get_text().split(',')[1].strip() if soup else ''  # 获取用户昵称
    info_list = [re.sub(r'\s+', '', i.text) for i in
                 soup.select('div.row div.card-wrap > div.card-body')] if soup else []  # 用户信息
    use_flow = soup.select('ol.breadcrumb > li')[1].text.split(':')[1].strip() if soup else ''  # 今日已用流量
    if info_list:
        info_list.insert(0, nick_name)
        info_list.insert(2, use_flow)
        return info_list
    else:
        return []


def iku_login_on(login, password):
    """ikuu登录信息"""
    session = requests.session()
    login_url = 'https://ikuuu.me/auth/login'
    data = {'email': login, 'passwd': password}
    response = get_response(session, method='post', url=login_url, data=data)
    flag, data = check_result(response)
    if flag:
        logger.info(f"ikuu登录情况：{data['msg']}")
        return session
    else:
        logger.info(f"ikuu登录情况：{data['msg']}")
        logger.info('程序退出！')
        exit()


def xk_sign_in(session):
    """ikuu签到信息"""
    sign_url = 'https://ikuuu.me/user/checkin'
    response = get_response(session, method='post', url=sign_url)
    flag, data = check_result(response)
    if flag:
        logger.info(f"ikuu签到情况：签到成功[{data['msg']}]!")
    else:
        logger.info(f"ikuu签到情况：签到失败[{data['msg']}]!")


def iku_userinfo(session):
    """ikuu用户信息"""
    user_url = 'https://ikuuu.me/user'
    response = get_response(session, url=user_url)
    info_list = parse_html(response)
    if info_list:
        logger.info('ikuu用户信息：用户昵称：{},会员时长：{},今日已用：{}\nikuu用户信息：可用流量：{},在线设备：{},钱包余额：{}'.format(*info_list))
    else:
        logger.info(f'ikuu用户信息：获取用户信息数据失败!')


def iku_usersubscribe(session):
    """ikuu的订阅信息"""
    subscribe_url = 'https://ikuuu.me/user/tutorial?os=windows&client=cfw'
    response = get_response(session, url=subscribe_url)
    text = response.text if response else ''
    link_text = re.search(r"oneclickImport\('clash', '(.*?)'\)", text)
    if link_text:
        logger.info(f'ikuu【clash】订阅：{link_text.group(1)}')
    else:
        logger.info('ikuu【clash】订阅：获取失败!')


def main():
    # login, password = iku_account_info()
    session = iku_login_on(iku_login, iku_password)
    iku_userinfo(session)
    iku_usersubscribe(session)
    # xk_sign_in(session)
    send_ding('ikuu代理签到')


if __name__ == '__main__':
    main()
