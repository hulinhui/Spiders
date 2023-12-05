# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         Acfun
# Description:  
# Author:       hlh
# Date:      2023/11/27 10:21
# -------------------------------------------------------------------------------

import requests
from py0314.FormatHeaders import get_format_headers, header_af
from py0314.NotifyMessage import read_config, send_ding
from py0314.loggingmethod import get_logging


class AcFun:
    def __init__(self):
        self.ac_phone, self.ac_password = read_config()['ACFUN'].values()
        self.headers = get_format_headers(header_af)
        self.logger = get_logging()
        self.session = requests.session()

    def get_response(self, url, method='get', headers=None, data=None):
        try:
            response = self.session.request(method=method, url=url, headers=headers, data=data)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response
        except Exception as e:
            self.logger.info(e)

    @staticmethod
    def check_response(response, return_value=None):
        json_data = {} if response is None else response.json()
        data = json_data['result'] if json_data and 'result' in json_data else 1
        result = True if data == 0 else False
        if return_value:
            return result
        else:
            return result, json_data

    def af_login(self):
        login_url = 'https://id.app.acfun.cn/rest/web/login/signin'
        data = {'username': self.ac_phone, 'password': self.ac_password}
        response = self.get_response(url=login_url, method='POST', headers=self.headers, data=data)
        flag, data = self.check_response(response)
        if not flag:
            self.logger.info('【ACFUN】登录情况:登录失败!')
            return
        self.logger.info(f"【ACFUN】登录情况:用户[{data['username']}]登录成功!")

    def af_signin(self):
        sign_url = 'https://www.acfun.cn/rest/pc-direct/user/signIn'
        self.headers['Host'] = 'www.acfun.cn'
        response = self.get_response(url=sign_url, headers=self.headers)
        flag, data = self.check_response(response)
        self.logger.info(f"【ACFUN】签到情况:{data['msg']}!")

    def af_info(self):
        info_url = 'https://www.acfun.cn/rest/pc-direct/user/personalInfo'
        response = self.get_response(url=info_url, headers=self.headers)
        flag, data = self.check_response(response)
        if not flag:
            self.logger.info('【ACFUN】用户信息:获取失败!')
            return
        ba_sum = data['info']['banana']
        gold_ba_sum = data['info']['goldBanana']
        self.logger.info(f"【ACFUN】用户信息:香蕉[{ba_sum}个],金香蕉[{gold_ba_sum}个]")

    def run(self):
        self.af_login()
        self.af_signin()
        self.af_info()
        send_ding('AcFun', mode=0)


if __name__ == '__main__':
    af = AcFun()
    af.run()
