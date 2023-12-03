# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         xiongmao
# Description:  
# Author:       hlh
# Date:      2023/10/31 14:15
# -------------------------------------------------------------------------------
import os

import requests
from py0314.FormatHeaders import headers_xiongmao, get_format_headers
from py0314.NotifyMessage import send_ding, read_config
from py0314.loggingmethod import get_logging

headers = get_format_headers(headers_xiongmao)
logger = get_logging()


def xm_account_info():
    """环境变量中获取数据"""
    params_list = ['xom_login', 'xom_password', 'xom_is_run', 'xom_gift_name']
    real_params = [os.environ[params] for params in params_list if params in os.environ and os.environ.get(params)]
    if len(real_params) != len(params_list):
        logger.info('熊猫代理缺少可执行的参数！')
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
    result = json_data['code'] if json_data and 'code' in json_data else ''
    is_login = True if result == '0' else False
    if check_login:
        return is_login
    else:
        return is_login, json_data


def xm_login(account, password):
    """熊猫先登录获取session"""
    session = requests.session()
    login_url = 'http://www.xiongmaodaili.com/xiongmao-web/user/login'
    data = {'account': account, 'password': password, 'originType': '1'}
    response = get_response(session, method='post', url=login_url, data=data)
    if check_result(response, True):
        return session
    else:
        logger.info('登录失败！')
        logger.info('程序退出！')
        exit()


def xm_userinfo(session):
    """获取用户个人信息"""
    userinfo_url = 'http://www.xiongmaodaili.com/xiongmao-web/user/userInfo'
    # session.headers.update({'X-Requested-With': 'XMLHttpRequest'})
    response = get_response(session, url=userinfo_url)
    flag, data = check_result(response)
    if flag:
        logger.info(f"账户信息:{data['obj']['userName']}；登录账号：{data['obj']['mobile']}；"
                    f"账户金额：{data['obj']['money']}；账户积分：{data['obj']['points']}")
        # return data['obj']['secret']
    else:
        logger.info('用户信息数据获取失败！')


def xm_userpoints(session):
    """查询用户积分"""
    points_url = 'http://www.xiongmaodaili.com/xiongmao-web/points/getUserPoints'
    response = get_response(session, url=points_url)
    flag, data = check_result(response)
    if flag:
        return int(data['obj'])
    else:
        logger.info('用户积分数据获取失败！')


def xm_luckdraw(session):
    luckDraw_url = 'http://www.xiongmaodaili.com/xiongmao-web/points/luckDraw'
    response = get_response(session, url=luckDraw_url)
    flag, data = check_result(response)
    if flag:
        logger.info(f"抽奖结果:{data['obj']}")
    else:
        logger.info('抽奖结果:积分不足！')


def xm_real_sign(session, sign_status, day):
    """先判断今天是否签到，再进行签到，签到完成后查询连续签到天数"""
    sign_url = f'http://www.xiongmaodaili.com/xiongmao-web/points/receivePoints?signInDay={day}'
    if sign_status == 0:
        logger.info('今日未签到，执行签到操作！')
        response = get_response(session, url=sign_url)
        flag = check_result(response, True)
        if flag:
            logger.info('签到情况：今日签到成功！')
        else:
            logger.info('签到情况：今日已签到！')
    else:
        logger.info('签到情况：今日已签到！')


def xm_signday_time(session):
    sindaytime_url = 'http://www.xiongmaodaili.com/xiongmao-web/points/getSignInDayTime'
    response = get_response(session, url=sindaytime_url)
    flag, data = check_result(response)
    if flag:
        logger.info(f"连续签到结果：已连续签到{data['obj']}天")
    else:
        logger.info('连续签到结果：获取连续签到天数失败！')


def xm_sign_data(session):
    signday_url = 'http://www.xiongmaodaili.com/xiongmao-web/points/getSignInDay'
    response = get_response(session, url=signday_url)
    flag, data = check_result(response)
    if flag:
        sign_day, sign_status = \
            [(index, item['status']) for index, item in enumerate(data.get('obj'), 1) if item['date'] == '今日'][0]
        xm_real_sign(session, sign_status, sign_day)
        xm_signday_time(session)
    else:
        logger.info('获取签到信息失败！')


def xm_get_whitelist(secret):
    whitelist_url = f'http://www.xiongmaodaili.com/xiongmao-web/clientWhilteList/listUserIp?secret={secret}'
    response = requests.get(whitelist_url)
    flag, data = check_result(response)
    if flag:
        white_list = [item['ip'] for item in data['obj']]
        return white_list[0]
    else:
        logger.info('获取白名单列表失败')


def xm_del_whitelist(secret, ip):
    whitelist_url = f'http://www.xiongmaodaili.com/xiongmao-web/whilteList/delIp?secret={secret}&ip={ip}'
    response = requests.get(whitelist_url)
    flag = check_result(response, True)
    if flag:
        logger.info('删除白名单ip成功')
    else:
        logger.info('删除白名单ip失败')


def xm_add_whitelist(secret, ip, orderno):
    whitelist_url = f'http://www.xiongmaodaili.com/xiongmao-web/whilteList/addOrUpdate?orderNo={orderno}&secret={secret}&newIp={ip}'
    response = requests.get(whitelist_url)
    flag = check_result(response, True)
    if flag:
        logger.info('白名单ip添加成功')
    else:
        logger.info('白名单ip添加失败')


def xm_update_whitelist(secret, oldip, orderno, newip):
    whitelist_url = f'http://www.xiongmaodaili.com/xiongmao-web/whilteList/addOrUpdate?orderNo={orderno}&secret={secret}&oldIp={oldip}&newIp={newip}'
    response = requests.get(whitelist_url)
    flag = check_result(response, True)
    if flag:
        logger.info('白名单ip更新成功')
    else:
        logger.info('白名单ip更新失败')


def xm_localhost_ip():
    myip_url = f'https://myip.ipip.net/json'
    response = requests.get(myip_url)
    return response.json()['data']['ip']


def xm_taskdone(session):
    task_list = 'http://www.xiongmaodaili.com/xiongmao-web/points/getTaskList'
    response = get_response(session, task_list)
    flag, data = check_result(response)
    if flag:
        logger.info(f"任务赚积分：总共有{len(data['obj'])}个任务")
        for item in data['obj']:
            done_text = '已完成' if item['isDone'] == 2 else '未完成'
            logger.info(f"{item['channelName']}【{item['point']}积分】:{done_text}")
    else:
        logger.info('任务列表获取失败！')


def xm_get_giftinfo(session, gift_name):
    gift_list_url = 'http://www.xiongmaodaili.com/xiongmao-web/points/listPointsGoods?pageNum=1&type=1%2C2'
    response = get_response(session, gift_list_url)
    flag, data = check_result(response)
    if flag:
        gift_list = data.get('obj').get('list')
        gift_data = [(item['id'], item['point']) for item in gift_list if item['goodsName'] == gift_name]
        if not gift_data:
            logger.info('权益商品不存在！')
            return None
        return gift_data[0]

    else:
        logger.info('权益数据列表获取失败！')


def xm_exchange_gift(session, gift_id, gift_name):
    exchange_good_url = f'http://www.xiongmaodaili.com/xiongmao-web/points/exchangeGoods?goodsId={gift_id}'
    response = get_response(session, exchange_good_url)
    flag, data = check_result(response)
    if flag:
        logger.info(f"兑换权益[{gift_name}]:兑换成功【{data['msg']}】！")
    else:
        logger.info(f"兑换权益[{gift_name}]:兑换失败【{data['msg']}】!")


def xm_check_and_exchange_gift(session, gift_name):
    user_point = xm_userpoints(session)
    gift_info = xm_get_giftinfo(session, gift_name)
    if gift_info and int(gift_info[1]) > user_point:
        xm_exchange_gift(session, gift_info[0], gift_name)
    else:
        logger.info(f'兑换权益[{gift_name}]:积分不足或商品异常!')


def main():
    xm_info = read_config()['XIONGMAO']
    session = xm_login(xm_info['xm_account'], xm_info['xm_password'])  # 登录
    xm_userinfo(session)  # 获取用户信息
    ######################白名单部分########################################################
    # xm_secret = xm_userinfo(session)
    # lat_ip = xm_localhost_ip()
    # white_ip = xm_get_whitelist(xm_secret)  # 获取白名单列表
    # xm_del_whitelist(xm_secret, '113.110.172.219')
    # xm_add_whitelist(xm_secret, '113.110.172.219', 'SDL20231031174345afjngqwO')
    # xm_update_whitelist(xm_secret, white_ip, 'SDL20231031174345afjngqwO', lat_ip)
    #######################################################################################
    xm_sign_data(session)  # 签到
    xm_userpoints(session)  # 获取用户积分
    xm_taskdone(session)  # 任务完成情况
    if xm_info['xm_is_run'] == 'true':
        xm_luckdraw(session)  # 熊猫抽奖
    xm_check_and_exchange_gift(session, xm_info['xm_gift_name'])  # 兑换权益
    send_ding('熊猫代理签到')


if __name__ == '__main__':
    main()
