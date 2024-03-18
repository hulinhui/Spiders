# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         ql_profile
# Description:  
# Author:       hlh
# Date:      2023/11/22 13:57
# -------------------------------------------------------------------------------
import time
import os
from ql_token import QL_token


class QL_PROFILE:
    def __init__(self):
        self.ql_info = QL_token()
        self.ql_info.get_token()
        self.files_url_format = '{}/open/configs/{}?t={}'
        self.filename = self.ql_info.ql_config['ql_jd_filename']
        self.content = self.ql_info.ql_config['ql_jd_variable']

    def all_files(self, filename='files'):
        file_url = self.files_url_format.format(self.ql_info.host, filename, int(time.time() * 1000))
        response = self.ql_info.get_response(url=file_url, headers=self.ql_info.headers)
        result, data = self.ql_info.check_response(response)
        if result:
            result_data = data['data'] if data and 'data' in data else ''
            if isinstance(result_data, str):
                self.ql_info.logger.info(f"【青龙面板】配置文件-{filename}:获取成功✅")
                return result_data
            self.ql_info.logger.info("【青龙面板】所有配置文件获取成功✅")
            return list(map(lambda item: item['value'], result_data))
        else:
            self.ql_info.logger.info("【青龙面板】配置文件获取失败❌")

    def save_file(self, content):
        save_url = self.files_url_format.format(self.ql_info.host, 'save', int(time.time() * 1000))
        save_data = {"content": content, "name": self.filename}
        response = self.ql_info.get_response(url=save_url, method='post', headers=self.ql_info.headers, data=save_data)
        result = self.ql_info.check_response(response, True)
        if result:
            self.ql_info.logger.info(f"【青龙面板】配置文件-{self.filename}:保存成功✅")
        else:
            self.ql_info.logger.info(f"【青龙面板】配置文件-{self.filename}:保存失败❌")

    def update_text(self, file_text):
        aa_list = [line for line in file_text.strip().split('\n') if line]
        aa_list.extend(self.content.strip().split('|'))
        text = '\n'.join(aa_list)
        return text

    def download_file(self, text):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        cur_path = os.path.join(cur_dir, 'config')
        file_path = os.path.join(cur_path, 'config.txt')
        if not os.path.exists(cur_path):
            os.mkdir(cur_path)
        with open(file_path, 'w', encoding='utf-8') as fp:
            fp.write(text)
        print('本地配置文件下载成功！')

    def get_save_file(self):
        name_list = self.all_files()  # 查询所有文件名称
        if name_list and self.filename in name_list:
            text = self.all_files(self.filename)  # 获取文件内容
            self.download_file(text)
            # content = self.update_text(text)  # 文本处理方法
            # self.save_file(content)
        else:
            self.ql_info.logger.info('【青龙面板】文件名有误或者配置文件不存在❌')


if __name__ == '__main__':
    qp = QL_PROFILE()
    qp.get_save_file()
