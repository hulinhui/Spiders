# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         BatchCancelOrder
# Description:  
# Author:       hlh
# Date:      2023/5/24 20:53
# -------------------------------------------------------------------------------
from git_file.py0314.job_51.FormatHeaders import get_format_headers
import requests
import time
import random
import math
import string
import hashlib
import json
import re


class Batch_Order:
    # {"id_":1060991,"mod_time_":"2023-05-24 17:22:46","invalid_remark_":"1"}
    def __init__(self):
        self.order_list_url = 'https://distribution.gotokeep.com/v1/sale/saleOrder/searchList?'
        self.order_cancel_url = 'https://distribution.gotokeep.com/v1/sale/saleOrder/invalid'
        self.order_delete_url = 'https://distribution.gotokeep.com/v1/sale/saleOrder/delete'
        self.headers = get_format_headers()

    def get_params_str(self, search_params=None):
        if not search_params:
            search_params = {'ascending': 'asc', 'commit_time_end_': '2023-05-24', 'commit_time_start_': '2023-05-24',
                             'currentPage': '1', 'form_status_': '11-21-31-41-51-61-71', 'keyword_': '扬州亿果电子商务有限公司',
                             'showCount': '250'}
        return ''.join([k + v for k, v in search_params.items()]), search_params

    @staticmethod
    def get_md5_str(text):
        return hashlib.md5(text.encode()).hexdigest()

    def get_real_headers(self, params_str):
        if isinstance(params_str, dict):
            mod_time_ = params_str['mod_time_']
            json_str = json.dumps(params_str, ensure_ascii=False).replace(' ', '')
            params_str = re.sub('\d{4}-\d{2}-\d{4}:\d{2}:\d{2}', mod_time_, json_str)
        elif params_str:
            params_str = params_str
        else:
            params_str = ''
        timestamp = str(int(time.time() * math.pow(10, 7)))
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, 20))
        print(params_str)
        checkKey = 'yunshang' + self.headers['yunshl_token'] + timestamp + random_str + params_str
        self.headers['timestamp'] = timestamp
        self.headers['nonce'] = random_str
        self.headers['signnatrue'] = self.get_md5_str(checkKey)

    def get_response(self, method, url, params_dict=None, data_dict=None):
        try:
            response = requests.request(method, url=url, headers=self.headers, params=params_dict,
                                        data=data_dict)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response
        except Exception as e:
            print(e)
            exit()

    def get_order_info(self, response):
        json_data = response.json()
        if json_data['status'] == 1:
            data = json_data['data']
            if data.get('totalResult', 0) > 0:
                if data.get('pdList'):
                    for order in data['pdList']:
                        yield order['id_'], order['mod_time_']
                else:
                    order_msg = f"订单号-{data['code_']}：作废成功" if data.get(
                        'form_status_') == 999 else f"订单号-{data['code_']}：作废失败！"
                    print(order_msg)
            else:
                print('查询无订单！')
                exit()
        else:
            print('查询订单列表数据失败！')
            exit()

    def run(self):
        search_params_str, params_dict = self.get_params_str()
        self.get_real_headers(search_params_str)
        response = self.get_response('get', self.order_list_url, params_dict)
        for index, info in enumerate(self.get_order_info(response), 4):
            cancel_params = {"id_": info[0], "mod_time_": info[1], "invalid_remark_": f"0524作废订单-{index}"}
            self.get_real_headers(cancel_params)
            cancel_response = self.get_response('post', self.order_cancel_url, data_dict=cancel_params)
            self.get_order_info(cancel_response)
            break
        else:
            print('全部订单取消完成！')


if __name__ == '__main__':
    order = Batch_Order()
    order.run()
