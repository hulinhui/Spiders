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
from urllib.parse import unquote, quote
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

    def post_info(self):
        post_response = self.get_response(self.post_url)
        href_tuple = ('tbody[id*=normalthread] td.icn > a', 'href')
        detail_url = self.base_url + self.parse_html(post_response, href_tuple)
        if not detail_url:
            self.logger.info('详情页获取失败!')
            return
        return detail_url

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

    def get_dict_data(self, key_tup, value_tup, response, item):
        key_list = self.parse_html(response, key_tup, top=-1)
        value_list = self.parse_html(response, value_tup, top=-1)
        data = dict(zip(key_list, value_list))
        data.update(item)
        data_text = '&'.join([f'{key}={value.strip()}' for key, value in data.items()])
        return data_text

    def get_score_data(self, response):
        score_item = {'score2': '1', 'score6': '1', 'reason': quote('谢谢@Thanks！', encoding='gbk')}
        key_tuple = ('input[type=hidden]', 'name')
        value_tuple = ('input[type=hidden]', 'value')
        score_data = self.get_dict_data(key_tuple, value_tuple, response, score_item)
        return score_data

    def detail_info(self, response):
        ptid_tuple = ('a#ak_rate', 'onclick')
        title_tuple = ('span#thread_subject', 'text')
        text = self.parse_html(response, ptid_tuple)
        post_title = self.parse_html(response, title_tuple)
        if not (text and post_title):
            self.logger.info('详情页获取评分参数失败!')
        params_list = re.findall(r"'(.*?)'", text)[:2]
        params_url = f'{self.base_url}{params_list[1]}&t={int(time.time() * 1000)}&infloat=yes' \
                     f'&handlekey={params_list[0]}&inajax=1&ajaxtarget=fwin_content_{params_list[0]}'
        return params_url, post_title

    def send_score(self, detail_response):
        url, title = self.detail_info(detail_response)
        self.logger.info(f'免费评分：{title}')
        data_response = self.get_response(url)
        score_url = self.get_score_url(data_response)
        score_data = self.get_score_data(data_response)
        print(score_data)
        if not (score_url and score_data):
            self.logger.info('评分参数获取失败！')
            return
        score_response = self.get_response(score_url, method='POST', data=score_data)
        score_text = score_response.text
        if 'succeedhandle_rate' in score_text:
            reason = re.search("\s'(.*?)',\s{}\);", score_text, re.S).group(1)
        else:
            reason = re.search("CDATA\[(.*?)<", score_text, re.S).group(1)
        self.logger.info(reason)

    def get_comment_url(self, response):
        comment_tuple = ('#fastpostform', 'action')
        url_text = self.parse_html(response, comment_tuple)
        comment_url = f'{self.base_url}{url_text}&inajax=1'
        return comment_url

    def get_comment_data(self, response):
        comment_item = {'message': quote('感谢分享{:1_893:}', encoding='gbk')}
        key_tuple = ('td.plc > input', 'name')
        value_tuple = ('td.plc > input', 'value')
        comment_data = self.get_dict_data(key_tuple, value_tuple, response, comment_item)
        return comment_data

    def send_comment(self, response):
        comment_url = self.get_comment_url(response)
        comment_data = self.get_comment_data(response)
        print(comment_data)
        comment_response = self.get_response(comment_url, method='POST', data=comment_data)
        comment_text = comment_response.text
        if 'succeedhandle_fastpost' in comment_text:
            reason = re.search("\s'(.*?)',\s{", comment_text, re.S).group(1)
        else:
            reason = re.search("CDATA\[(.*?)<", comment_text, re.S).group(1)
        self.logger.info(reason)

    def run(self):
        post_url = self.post_info()  # 详情页url
        detail_response = self.get_response(post_url)  # 详情页响应数据
        self.send_score(detail_response)  # 免费评分
        self.send_comment(detail_response)  # 评论文章


if __name__ == '__main__':
    pojie_52 = Pojie()
    pojie_52.run()
