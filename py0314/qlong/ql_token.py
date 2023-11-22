# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         ql_token
# Description:  
# Author:       hlh
# Date:      2023/11/21 10:20
# -------------------------------------------------------------------------------
import json

import requests
from py0314.loggingmethod import get_logging
from py0314.NotifyMessage import read_config, send_ding
from py0314.FormatHeaders import get_format_headers, header_ql
import time


class QL_token:

    def __init__(self):
        self.ql_config = read_config()['QINGLONG']
        self.host = '{}:{}'.format(self.ql_config['ql_host'], self.ql_config['ql_port'])
        self.client_id = self.ql_config['ql_client_id']
        self.client_secret = self.ql_config['ql_client_secret']
        self.jd_cookies = self.ql_config['ql_jd_cookies']
        self.headers = get_format_headers(header_ql)
        self.logger = get_logging()

    def get_response(self, url, method='get', headers=None, data=None):
        try:
            data = json.dumps(data) if data else data
            response = requests.request(method=method, url=url, headers=headers, data=data)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response
        except Exception as e:
            self.logger.info(e)

    @staticmethod
    def check_response(response, return_value=None):
        json_data = {} if response is None else response.json()
        data = json_data['code'] if json_data and 'code' in json_data else 0
        result = True if data == 200 else False
        if return_value:
            return result
        else:
            return result, json_data

    def get_token(self):
        token_url = f"{self.host}/open/auth/token?client_id={self.client_id}&client_secret={self.client_secret}"
        response = self.get_response(token_url, headers=self.headers)
        result, data = self.check_response(response)
        if result:
            invalid_date = time.strftime('%Y-%m-%d %H:%M', time.localtime(data['data']['expiration']))
            self.logger.info(f"【青龙面板】获取token成功✅,有效期至:{invalid_date}")
            self.headers.update({'Authorization': f"Bearer {data['data']['token']}"})
        else:
            self.logger.info("【青龙面板】获取token失败❌")


if __name__ == '__main__':
    ql = QL_token()
    ql.get_token()
    print(ql.headers)
