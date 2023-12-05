# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         yuyun.py
# Description:  
# Author:       hlh
# Date:      2023/11/7 17:49
# -------------------------------------------------------------------------------
import json
import os
import platform
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests
from py0314.FormatHeaders import headers_yy, get_format_headers
from py0314.NotifyMessage import send_ding, read_config
from py0314.loggingmethod import get_logging

headers = get_format_headers(headers_yy)
logger = get_logging()


def yy_account_info():
    """环境变量中获取数据"""
    params_list = ['yy_login', 'yy_password']
    real_params = [os.environ[params] for params in params_list if os.environ.get(params)]
    if len(real_params) != len(params_list):
        logger.info('雨云缺少可执行的参数！')
        exit()
    return real_params


def get_response(session, url, method='get', data=None):
    try:
        response = session.request(method=method, url=url, headers=headers, data=json.dumps(data))
        response.encoding = 'utf-8'
        if response.status_code > 400:
            response.raise_for_status()
        return response
    except Exception as e:
        logger.info(e)


def check_result(response, check_login=None):
    json_data = {} if response is None else response.json()
    result = json_data['code'] if json_data and 'code' in json_data else 0
    is_login = True if result == 200 else False
    if check_login:
        return is_login
    else:
        return is_login, json_data


def yy_login_on(login, password):
    """雨云登录信息"""
    session = requests.session()
    login_url = 'https://api.v2.rainyun.com/user/login'
    data = {"field": login, "is_with_api_key": True, "password": password}
    response = get_response(session, method='post', url=login_url, data=data)
    flag, data = check_result(response)
    if flag:
        session.headers.update({'x-api-key': data['data']})
        logger.info(f"【🎉🎉🎉 恭喜您鸭 🎉🎉🎉】执行登录: 登录成功✅")
        return session
    else:
        logger.info(f"【🎉🎉🎉 恭喜您鸭 🎉🎉🎉】执行登录:失败 ❌ 了呢 ,可能是:登录失败了！")
        exit()


def yy_sign_in(session):
    """yy签到信息"""
    sign_url = 'https://api.v2.rainyun.com/user/reward/tasks'
    data = {"task_name": "每日签到", "verifyCode": ""}
    response = get_response(session, method='post', url=sign_url, data=data)
    flag, data = check_result(response)
    if flag:
        logger.info(f"【🎉🎉🎉 恭喜您鸭 🎉🎉🎉】执行签到: 签到成功[{data['data']}]✅")
    else:
        logger.info(f"【🎉🎉🎉 恭喜您鸭 🎉🎉🎉】执行签到: 失败 ❌ 了呢 ,可能是:[{data['message']}]")


def yy_userinfo(session):
    """yy用户信息"""
    user_url = 'https://api.v2.rainyun.com/user/'
    response = get_response(session, url=user_url)
    flag, data = check_result(response)
    if flag:
        user_dict = {'name': data['data']['Name'], 'Money': data['data']['Money'], 'Points': data['data']['Points'],
                     'LastLoginArea': data['data']['LastLoginArea'], 'VIP_name': data['data']['VIP']['Title']}
        logger.info('【🎉🎉🎉 恭喜您鸭 🎉🎉🎉】获取信息:获取成功✅')
        logger.info(
            '用户昵称：{name},会员名称：{VIP_name},积分：{Points},金额：{Money},''最后登录：{LastLoginArea}'.format(**user_dict))
    else:
        logger.info('【🎉🎉🎉 恭喜您鸭 🎉🎉🎉】获取信息: 获取失败❌')


def yy_usercoupons(session):
    coupons_url = 'https://api.v2.rainyun.com/user/coupons/'
    response = get_response(session, url=coupons_url)
    flag, data = check_result(response)
    if flag:
        for item in data['data']:
            exp_date = datetime.strftime(datetime.fromtimestamp(item['exp_date']), '%Y-%m-%d')
            remain_day = (datetime.fromtimestamp(item['exp_date']).date() - datetime.now().date()).days
            logger.info(f"【🎉🎉🎉 恭喜您鸭 🎉🎉🎉】获取优惠券:获取成功✅，获得【{item['friendly_name']}-剩余{remain_day}天】,有效期至 {exp_date}")
    else:
        logger.info('【🎉🎉🎉 恭喜您鸭 🎉🎉🎉】获取优惠券: 获取失败❌')


def yy_get_itemdata(data, gift_list):
    gift_id_list = [str(item['id']) for item in data['data']]
    plat = platform.system().lower()
    if plat == 'linux' and os.environ.get('gift_str') is not None:
        os.putenv('gift_str', '&'.join(gift_id_list))
    if len(gift_id_list) <= 25:
        logger.info("【🎉🎉🎉 恭喜您鸭 🎉🎉🎉】获取礼品列表:获取成功✅，未发现新增的礼品信息")
        logger.info("【🎉🎉🎉 恭喜您鸭 🎉🎉🎉】获取礼品列表:获取成功✅，继续查询现有红包库存")
        item_red = {item['id']: item['available_stock'] for item in data['data'] if
                    '红包' in item['name'] and item['available_stock'] > 0}
        return item_red
    else:
        if '320' in gift_list:
            gift_list.remove('320')
        logger.info("【🎉🎉🎉 恭喜您鸭 🎉🎉🎉】获取礼品列表:获取成功✅，发现新增的礼品信息")
        item_red = {item['id']: item['available_stock'] for item in data['data'] if
                    item['available_stock'] > 0 and item['id'] not in gift_list}
        return item_red


def yy_get_reward_items(session, gift_list):
    reward_url = 'https://api.v2.rainyun.com/user/reward/items'
    response = get_response(session, url=reward_url)
    flag, data = check_result(response)
    if flag:
        item_red = yy_get_itemdata(data, gift_list)
        return item_red
    else:
        logger.info(f"【🎉🎉🎉 恭喜您鸭 🎉🎉🎉】获取礼品列表: 获取失败❌，可能是：{data['message']}")


def yy_exchange_gift(session, item_id):
    gift_url = 'https://api.v2.rainyun.com/user/reward/items'
    data = {"item_id": item_id}
    response = get_response(session, method='post', url=gift_url, data=data)
    flag, data = check_result(response)
    if flag:
        logger.info("【🎉🎉🎉 恭喜您鸭 🎉🎉🎉】获取礼品:获取成功✅")
    else:
        logger.info(f"【🎉🎉🎉 恭喜您鸭 🎉🎉🎉】获取礼品: 获取失败❌，可能是：{data['message']}")


def main():
    yy_info = read_config()['YUYUN']
    # login, password = yy_account_info()
    session = yy_login_on(yy_info['yy_login'], yy_info['yy_password'])
    yy_userinfo(session)
    yy_sign_in(session)
    yy_usercoupons(session)
    item_info = yy_get_reward_items(session, yy_info['yy_gift_list'])
    if item_info and yy_info['yy_is_exchange']:
        with ThreadPoolExecutor(max_workers=5) as executor:
            for item_id in item_info:
                executor.submit(yy_exchange_gift, session, item_id)
    else:
        logger.info("【🎉🎉🎉 恭喜您鸭 🎉🎉🎉】领取礼品: 领取失败❌，可能是：没有库存或者未开启兑换")
    send_ding('yy机场签到')


if __name__ == '__main__':
    main()
