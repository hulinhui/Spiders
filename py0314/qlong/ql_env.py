# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         ql_env
# Description:  
# Author:       hlh
# Date:      2023/11/21 11:41
# -------------------------------------------------------------------------------
import re
from ql_token import QL_token
import time


class QL_ENV:
    def __init__(self):
        self.ql_info = QL_token()
        self.ql_info.get_token()
        self.env_url = f'{self.ql_info.host}/open/envs?t={int(time.time() * 1000)}'
        self.key_name = ['id', 'value', 'status', 'remarks', 'name']

    def get_env_list(self):
        response = self.ql_info.get_response(self.env_url, headers=self.ql_info.headers)
        result, data = self.ql_info.check_response(response)
        if result:
            self.ql_info.logger.info(f"【青龙面板】环境变量获取成功✅")
            return list(
                map(lambda item: {key: item[key] for key in item if key in self.key_name},
                    data['data']))
        else:
            self.ql_info.logger.info("【青龙面板】环境变量获取失败❌")

    def add_env(self, name, value, remarks):
        data = [{"value": value, "name": name, "remarks": remarks}]
        response = self.ql_info.get_response(url=self.env_url, method='post', headers=self.ql_info.headers, data=data)
        result = self.ql_info.check_response(response, True)
        if result:
            self.ql_info.logger.info(f"【青龙面板】环境变量-{remarks}:添加成功✅")
        else:
            self.ql_info.logger.info(f"【青龙面板】环境变量-{remarks}:添加失败❌")

    def delete_env(self, env_id):
        response = self.ql_info.get_response(url=self.env_url, method='delete', headers=self.ql_info.headers,
                                             data=[env_id])
        result = self.ql_info.check_response(response, True)
        if result:
            self.ql_info.logger.info(f"【青龙面板】环境变量-{env_id}:删除成功✅")
        else:
            self.ql_info.logger.info(f"【青龙面板】环境变量-{env_id}:删除失败❌")

    def update_env(self, data):
        response = self.ql_info.get_response(url=self.env_url, method='put', headers=self.ql_info.headers, data=data)
        result = self.ql_info.check_response(response, True)
        if result:
            self.ql_info.logger.info(f"【青龙面板】环境变量-{data['remarks']}:更新成功✅")
        else:
            self.ql_info.logger.info(f"【青龙面板】环境变量-{data['remarks']}:更新失败❌")

    def disable_env(self, env_id):
        disable_env_url = f'{self.ql_info.host}/open/envs/disable?t={int(time.time() * 1000)}'
        response = self.ql_info.get_response(url=disable_env_url, method='put', headers=self.ql_info.headers,
                                             data=[env_id])
        result = self.ql_info.check_response(response, True)
        if result:
            self.ql_info.logger.info(f"【青龙面板】环境变量-{env_id}:禁用成功✅")
        else:
            self.ql_info.logger.info(f"【青龙面板】环境变量-{env_id}:禁用失败❌")

    def enable_env(self, env_id):
        enable_env_url = f'{self.ql_info.host}/open/envs/enable?t={int(time.time() * 1000)}'
        response = self.ql_info.get_response(url=enable_env_url, method='put', headers=self.ql_info.headers,
                                             data=[env_id])
        result = self.ql_info.check_response(response, True)
        if result:
            self.ql_info.logger.info(f"【青龙面板】环境变量-{env_id}:启用成功✅")
        else:
            self.ql_info.logger.info(f"【青龙面板】环境变量-{env_id}:启用失败❌")

    def get_update_env(self):
        value_list = list(
            map(lambda params: {'value': params.strip(),
                                'remarks': re.findall(r'pt_pin=(.*?);', params.strip())[0],
                                'name': 'JD_COOKIE'}, self.ql_info.jd_cookies.split('#')))
        env_list = list(filter(lambda item: item['name'] == 'JD_COOKIE', self.get_env_list()))
        for value_item in value_list:
            for env_item in env_list:
                env_value = re.findall(r'pt_pin=(.*?);', env_item['value'].strip())[0]
                if value_item['remarks'] != env_value:
                    continue
                value_item.update({'id': env_item['id']})
                self.update_env(value_item)  # 更新
                if env_item['status']:
                    self.enable_env(env_item['id'])  # 更新后启用环境变量
                break
            else:
                self.add_env(**value_item)  # 新增


if __name__ == '__main__':
    ql_env = QL_ENV()
    ql_env.get_update_env()
