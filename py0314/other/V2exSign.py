# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         V2exSign.py
# Description:
# Author:       hlh
# Date:      2023/11/23 14:37
# -------------------------------------------------------------------------------
import re

import requests
from py0314.FormatHeaders import get_format_headers, header_v2
from py0314.NotifyMessage import read_config, send_ding
from py0314.loggingmethod import get_logging
from requests import exceptions
from tenacity import retry, retry_if_exception_type, wait_fixed, stop_after_attempt

logger = get_logging()
header = get_format_headers(header_v2)


class V2_Sign:
    def __init__(self):
        self.page_url = 'https://www.v2ex.com/mission/daily'
        self.logger = get_logging()
        self.header = self.update_header()

    @staticmethod
    def update_header():
        cookies_text = read_config()['V2EX']['v2_cookie']
        header_dict = get_format_headers(header_v2.format(cookies_text))
        return header_dict

    @retry(retry=retry_if_exception_type((exceptions.Timeout, exceptions.ProxyError, exceptions.ReadTimeout)),
           reraise=True,
           retry_error_callback=exit,
           wait=wait_fixed(3), stop=stop_after_attempt(3))
    def get_response(self, url):
        response = requests.get(url=url, headers=self.header, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response

    def parse_html(self, response):
        if not response:
            self.logger.info('【V2EX】页面数据获取失败！')
            return
        text = response.text
        message_text = re.search('<span.*?gray"><li.*?/li>.*?;(.*?)</span>', text, re.S).group(1)
        sign_day_text = re.sub(r'\s+', '', re.findall('<div class="cell">(.*?)</div>', text, re.S)[-1])
        ag, cu = re.findall('<a.*?balance_area.*?>(.*?)<.*?/>(.*?)<img.*?</a>', text, re.S)[0]
        sign_text = f'【V2EX】签到情况:{message_text},{sign_day_text},账户余额：{ag.strip()}个银币,{cu.strip()}个铜币'
        self.logger.info(sign_text)

    def get_sign_url(self, response):
        link_data = re.search('<input type="button.*?location.href = \'(.*?)\';" />', response.text, re.S)
        sign_url = self.page_url.split('/m')[0] + link_data.group(1) if link_data else ''
        return sign_url

    def run(self):
        try:
            self.logger.info('【V2EX】签到情况：')
            page_response = self.get_response(self.page_url)
            sign_url = self.get_sign_url(page_response)
            if not sign_url:
                self.logger.info('【V2EX】签到链接获取失败！')
            elif sign_url.endswith('balance'):
                self.logger.info('【V2EX】今日无需签到！')
                self.parse_html(page_response)
            else:
                self.logger.info('【V2EX】开始执行签到！')
                result_response = self.get_response(sign_url)
                self.parse_html(result_response)
        except Exception as e:
            self.logger.info(f'【V2EX】发生错误:{e}！')
        finally:
            send_ding('V2EX签到')


if __name__ == '__main__':
    v2ex = V2_Sign()
    v2ex.run()
