# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         JuLiang.py
# Description:  
# Author:       hulinhui779
# Date:      2024/1/17 10:40
# -------------------------------------------------------------------------------
import os
import requests
from bs4 import BeautifulSoup
from py0314.FormatHeaders import header_jl, get_format_headers
from py0314.NotifyMessage import send_ding, read_config
from py0314.logger_tools.Handle_Logger import HandleLog
import hashlib


class JuLiang_Ip:

    def __init__(self):
        self.session = self.__jl_session()
        self.logger = HandleLog()
        self.acount_info = self.__jl_account_info()

    @staticmethod
    def __jl_session():
        """给会话设置请求头信息"""
        session = requests.session()
        header_dict = get_format_headers(header_jl)
        session.headers = header_dict
        return session

    def __jl_account_info(self):
        """判断当前系统，执行对应获取信息的方法"""
        if os.name == 'nt':
            return list(read_config()['JULIANG'].values())
        else:
            return self.__linux_account()

    def __linux_account(self):
        """环境变量中获取数据"""
        params_list = ['jl_login', 'jl_password']
        real_params = [os.environ[params] for params in params_list if params in os.environ and os.environ.get(params)]
        if len(real_params) != len(params_list):
            self.logger.error('巨量代理缺少可执行的参数！')
            exit()
        return real_params

    def __jl_request(self, url, method='GET', params=None, data=None):
        """接口请求"""
        try:
            response = self.session.request(method=method, url=url, params=params, data=data)
            response.raise_for_status()
        except Exception as e:
            self.logger.error(e)
        else:
            response.encoding = response.apparent_encoding
            return response

    @staticmethod
    def __result_params(key, val, status=False):
        result_dict = {'res_key': key, 'res_val': val, 'only_status': status}
        return result_dict

    @staticmethod
    def __check_json_result(response, **kwargs):
        """校验请求json响应返回结果"""
        json_data = response.json() if response else {}
        result = json_data[kwargs['res_key']] if json_data and kwargs['res_key'] in json_data else ''
        is_success = True if str(result) == kwargs['res_val'] else False
        if kwargs['only_status']:
            return is_success
        else:
            return is_success, json_data

    @staticmethod
    def __check_text_result(response, only_status=False):
        """校验请求text响应返回结果"""
        text = response.text if response else ''
        is_success = True if text.startswith('<!DOCTYPE html>') else False
        real_text = text if is_success else ''
        if only_status:
            return is_success
        else:
            return is_success, real_text

    def jl_login(self):
        """登录"""
        jl_login_url = 'https://www.juliangip.com/login/go'
        login_data = {'type': 'password', 'username': self.acount_info[0], 'password': self.acount_info[1]}
        jl_login_response = self.__jl_request(url=jl_login_url, method='POST', data=login_data)
        jl_result_dict = self.__result_params('state', 'ok')
        login_flag, login_info = self.__check_json_result(jl_login_response, **jl_result_dict)
        message_text = login_info.get('message', '失败') if login_flag and login_info else '失败'
        self.logger.info(f'巨量登录情况:登录{message_text}!')

    def jl_order_no(self):
        """获取订单号"""
        jl_user_url = 'https://www.juliangip.com/users/'
        jl_user_response = self.__jl_request(url=jl_user_url)
        jl_is_success, jl_response_text = self.__check_text_result(jl_user_response)
        jl_soup = BeautifulSoup(jl_response_text, 'lxml')
        jl_td_soup = jl_soup.select_one('div.pro_card tbody td')
        order_no = jl_td_soup.get_text() if jl_td_soup else None
        return order_no

    def jl_get_key(self, jl_order_no):
        """获取订单相关的api_key"""
        if not jl_order_no:
            self.logger.warning('订单号获取失败')
            return
        jl_order_url = f'https://www.juliangip.com/order/info?trade_no={jl_order_no}'
        jl_order_response = self.__jl_request(url=jl_order_url)
        jl_result_dict = self.__result_params('state', 'ok')
        jl_is_success, jl_order_data = self.__check_json_result(jl_order_response, **jl_result_dict)
        if jl_is_success and jl_order_data:
            return jl_order_data.get('data', {}).get('key', None)
        else:
            self.logger.warning('订单apikey获取失败!')

    @staticmethod
    def jl_get_sign(params_dict, secret):
        """实现接口参数加密并返回params"""
        params_text = '&'.join([f'{key}={value}' for key, value in sorted(params_dict.items())]) + f'&key={secret}'
        sign = hashlib.md5(params_text.encode()).hexdigest()
        params_dict['sign'] = sign
        return params_dict

    def jl_order_balance(self, jl_order_no, jl_api_key):
        """剩余可提取ip数量"""
        jl_balance_url = 'http://v2.api.juliangip.com/dynamic/balance'
        params_dict = {'trade_no': jl_order_no}
        order_params = self.jl_get_sign(params_dict, jl_api_key)
        jl_balance_response = self.__jl_request(url=jl_balance_url, params=order_params)
        jl_result_dict = self.__result_params('code', '200')
        jl_is_success, jl_balance_data = self.__check_json_result(jl_balance_response, **jl_result_dict)
        if jl_is_success and jl_balance_data:
            return jl_balance_data.get('data', {}).get('balance', None)
        else:
            self.logger.warning('订单剩余可提取ip数获取失败！')

    def jl_order_ip_balance(self):
        """
        1、获取订单号【首页-待续费订单-订单号】
        2、根据单号查询对应的api密钥
        3、调用api文案内的查询剩余可提取IP的数量
        """
        jl_order_no = self.jl_order_no()
        jl_api_key = self.jl_get_key(jl_order_no)
        if not (jl_order_no and jl_api_key):
            self.logger.warning('订单号或者api_key参数异常!')
            return
        order_balance = self.jl_order_balance(jl_order_no, jl_api_key)
        if not order_balance:
            return
        self.logger.info(f'订单[{jl_order_no}]:剩余可提取ip数[{order_balance}]')

    def jl_run(self):
        self.jl_login()
        self.jl_order_ip_balance()
        send_ding('巨量代理')


if __name__ == '__main__':
    juliang = JuLiang_Ip()
    juliang.jl_run()
