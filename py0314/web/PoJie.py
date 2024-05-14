# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         PoJie.py
# Description:  
# Author:       hlh
# Date:      2024/5/14 15:37
# -------------------------------------------------------------------------------
import re
import time
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
from py0314.FormatHeaders import headers_52, get_format_headers
from py0314.loggingmethod import get_logging


class Pojie:
    def __init__(self):
        self.post_url = 'https://www.52pojie.cn/forum.php?mod=forumdisplay&fid=16&filter=author&orderby=dateline&typeid=231'
        self.base_url = self.post_url.rsplit('/', 1)[0] + '/'
        self.headers = get_format_headers(headers_52)
        self.logger = get_logging()

    def get_response(self, url, method='get', data=None):
        try:
            response = requests.request(method=method, url=url, headers=self.headers, data=data)
            response.raise_for_status()
            response.encoding = 'gbk'
            return response
        except Exception as e:
            self.logger.info(e)

    def parse_html(self, response, seletor_tuple, top=0):
        result_text = response.text if response else ''
        soup = BeautifulSoup(result_text, 'lxml')
        if not soup: return
        if top < 0:
            return [_.get(seletor_tuple[1]) for _ in soup.select(seletor_tuple[0])]
        if seletor_tuple[1] != 'text':
            return soup.select(seletor_tuple[0])[top].get(seletor_tuple[1])
        return soup.select(seletor_tuple[0])[top].get_text()

    def get_score_url(self, response):
        if 'errorhandle_rate' in response.text:
            url_text = re.search("errorhandle_rate\('(.*?)',\s{}\);", response.text, re.S).group(1)
        else:
            score_tuple = ('#rateform', 'action')
            url_text = self.parse_html(response, score_tuple)
        if sum([1 if u'\u4e00' <= i <= u'\u9fff' else 0 for i in url_text]) > 0:
            self.logger.info(url_text)
            return
        score_url = f'{self.base_url}{url_text}&inajax=1'
        return score_url

    def get_score_data(self, response, item):
        key_tuple = ('input[type=hidden]', 'name')
        value_tuple = ('input[type=hidden]', 'value')
        key_list = self.parse_html(response, key_tuple, top=-1)
        value_list = self.parse_html(response, value_tuple, top=-1)
        data = dict(zip(key_list, value_list))
        data.update(item)
        return data

    def post_info(self):
        post_response = self.get_response(self.post_url)
        href_tuple = ('tbody[id*=normalthread] td.icn > a', 'href')
        detail_url = self.base_url + self.parse_html(post_response, href_tuple)
        if not detail_url:
            self.logger.info('详情页获取失败!')
            return
        return detail_url

    def detail_info(self, detail_url):
        detail_response = self.get_response(detail_url)
        ptid_tuple = ('a#ak_rate', 'onclick')
        title_tuple = ('span#thread_subject', 'text')
        text = self.parse_html(detail_response, ptid_tuple)
        post_title = self.parse_html(detail_response, title_tuple)
        if not (text and post_title):
            self.logger.info('详情页获取评分参数失败!')
        params_list = re.findall(r"'(.*?)'", text)[:2]
        params_url = f'{self.base_url}{params_list[1]}&t={int(time.time() * 1000)}&infloat=yes' \
                     f'&handlekey={params_list[0]}&inajax=1&ajaxtarget=fwin_content_{params_list[0]}'
        return params_url, post_title

    def send_score(self, detail_info):
        url, title = detail_info
        score_item = {'score2': '1', 'score6': '1', 'reason': quote('谢谢@Thanks！',encoding='gbk')}
        data_response = self.get_response(url)
        score_url = self.get_score_url(data_response)
        score_data = self.get_score_data(data_response, score_item)
        if not (score_url and score_data):
            self.logger.info('评分参数获取失败！')
            return
        score_response = self.get_response(score_url, method='POST', data=score_data)
        score_text = score_response.text
        if 'succeedhandle_rate' in score_text:
            reason = re.search("\s'(.*?)',\s{}\);", score_response.text, re.S).group(1)
        else:
            reason = re.search("CDATA\[(.*?)<", score_response.text, re.S).group(1)
        self.logger.info(reason)

    def run(self):
        post_url = self.post_info()
        detail_info = self.detail_info(post_url)
        self.send_score(detail_info)


if __name__ == '__main__':
    pojie_52 = Pojie()
    pojie_52.run()
