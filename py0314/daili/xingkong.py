# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         xingkong
# Description:  
# Author:       hlh
# Date:      2023/11/2 10:46
# -------------------------------------------------------------------------------
import os
import requests
from bs4 import BeautifulSoup
from py0314.FormatHeaders import headers_xingkong, get_format_headers
from py0314.loggingmethod import get_logging
from py0314.NotifyMessage import send_ding, read_config

headers = get_format_headers(headers_xingkong)
logger = get_logging()


def xk_account_info():
    """环境变量中获取数据"""
    params_list = ['xk_login', 'xk_password', 'xk_is_renew', 'xk_condition']
    real_params = [os.environ[params] for params in params_list if params in os.environ and os.environ.get(params)]
    if len(real_params) != len(params_list):
        logger.info('星空代理缺少可执行的参数！')
        exit()
    return real_params


def get_response(session, url, method='get', data=None):
    try:
        response = session.request(method=method, url=url, headers=headers, data=data, verify=False)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response
    except Exception as e:
        logger.info(e)


def check_result(response, check_login=None):
    json_data = response.json() if response else {}
    result = json_data['status'] if json_data and 'status' in json_data else ''
    is_login = True if result else False
    if check_login:
        return is_login
    else:
        return is_login, json_data


def parse_html(response, selector):
    text = response.text if response else ''
    soup = BeautifulSoup(text, 'html.parser')
    start_num = int(soup.select_one(selector).text) if soup else 0
    return start_num


def xk_login_on(login, password):
    """熊猫先登录获取session"""
    session = requests.session()
    login_url = 'http://www.xkdaili.com/tools/submit_ajax.ashx?action=user_login&site_id=1'
    data = {'username': login, 'password': password, 'remember': 1}
    response = get_response(session, method='post', url=login_url, data=data)
    flag, data = check_result(response)
    if flag:
        logger.info(f"星空登录情况：{data['msg']}")
        return session
    else:
        logger.info(f"星空登录情况：{data['msg']}")
        logger.info('程序退出！')
        exit()


def xk_sign_in(session):
    sign_url = 'http://www.xkdaili.com/tools/submit_ajax.ashx?action=user_receive_point'
    data_sign = {'type': 'login'}
    response = get_response(session, method='post', url=sign_url, data=data_sign)
    flag, data = check_result(response)
    if flag:
        logger.info(f"星空签到情况：签到成功[+{data['msg']['point']}积分]!")
    else:
        logger.info(f"星空签到情况：签到失败[{data['msg']}]")


def xk_get_starB(session):
    user_center_url = 'http://www.xkdaili.com/main/usercenter.aspx'
    response = get_response(session, url=user_center_url)
    starB_num = parse_html(response, 'span#star_B_Num')
    if starB_num:
        logger.info(f'星币总数：{starB_num}个')
    else:
        logger.info(f'星币总数：获取失败！')
    return starB_num


def parse_order_html(response):
    text = response.text if response else ''
    soup = BeautifulSoup(text, 'html.parser')
    ip_num = int(soup.select_one('tr.Receive_star_trbg > td:nth-last-of-type(3)').text) if soup else 0
    text = soup.select_one('tr.Receive_star_trbg > td > a:nth-of-type(1)').get('onclick') if soup else ''
    if not (text and ip_num):
        logger.info('获取订单信息失败！')
        return ip_num, []
    params_list = [eval(_.strip()) for _ in text.split(',')[1:4]]
    return ip_num, params_list


def xk_ip_residue(session, xk_is_renew, xk_condition):
    """获取套餐订单ip剩余量"""
    order_url = 'http://www.xkdaili.com/main/myOrders.aspx'
    response = get_response(session, url=order_url)
    ip_num, params_list = parse_order_html(response)
    if 0 < ip_num < int(xk_condition) and xk_is_renew:
        logger.info(f'ip余量【{ip_num}】小于{xk_condition}并且开启了自动续费,执行续费操作')
        starB_num = xk_get_starB(session)
        xk_starB_renew(session, starB_num, params_list)
    else:
        logger.info(f'ip余量：{ip_num}，不需要进行星币续费！')


def xk_starB_renew(session, star_num, datalist):
    renew_url = 'http://www.xkdaili.com/ashx/iporder/RenewOrder.ashx'
    orderId, orderCode, need_starB = datalist if datalist else [0, '', 0]
    if star_num > need_starB > 0:
        data = {'orderId': orderId, 'payment_id': 7, 'amount': need_starB}
        response = get_response(session, method='post', url=renew_url, data=data)
        flag, data = check_result(response)
        if flag:
            logger.info(f"订单-{orderCode}-星币续费结果:{data['msg']}")
        else:
            logger.info(f"订单-{orderCode}-星币续费结果:{data['msg']}")
    else:
        logger.info('星币续费结果：星币个数不足或者参数异常！')


def xk_ip_extract_count(session):
    ipcollect_url = 'http://www.xkdaili.com/main/IPCollect.aspx'
    response = get_response(session, url=ipcollect_url)
    ip_count = parse_html(response, 'span#ContentPlaceHolder_lbIPCount')
    if ip_count > 0:
        logger.info(f'星空ip日提取量:{ip_count}')
    else:
        logger.info(f'星空ip日提取量:今天未提取ip')


def main():
    xk_info = read_config()['XINGKONG']
    # login, password, is_renew, condition = xk_account_info()
    session = xk_login_on(xk_info['xk_login'], xk_info['xk_password'])
    xk_sign_in(session)
    xk_ip_extract_count(session)
    xk_ip_residue(session, xk_info['xk_is_renew'], xk_info['xk_condition'])
    send_ding('星空代理')


if __name__ == '__main__':
    main()
