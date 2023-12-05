# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         zhenhui_book
# Description:  
# Author:       hlh
# Date:      2022/3/18 14:36
# -------------------------------------------------------------------------------
import re

import requests
from lxml import etree


class ZhengHun():
    def __init__(self):
        self.top_url = "https://www.zhenhunxiaoshuo.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4911.0 Safari/537.36 Edg/101.0.1193.0"}

    def top_info(self):
        html = self.get_html(self.top_url)
        top_data = self.parse_top(html)
        return top_data

    def parse_top(self, html):
        if html:
            info_data=[]
            tree = etree.HTML(html.text)
            li_tree = tree.xpath('//ul[@id="sitenav"]/li')
            for li in li_tree:
                a_title = li.xpath('./a/text()')
                a_href = li.xpath('./a/@href')
                page_text = li.xpath('./ul[@class="sub-menu"]/li[last()]/a/text()')[0] if li.xpath('./ul') else '1'
                pattern = re.search('\d+', page_text)
                a_page_num = pattern.group(0) if pattern else "1"
                if a_title.endswith("小说") or a_title.endswith('作品集'):
                    info_data.append((a_title,a_href,a_page_num))
            return info_data

        else:
            return None

    def get_html(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response
        except Exception as e:
            print(e)

    def chun_ai(self):
        pass

    def yan_qing(self):
        pass

    def priest(self):
        pass

    def run(self):
        info_data = self.top_info()
        print(info_data)


if __name__ == '__main__':
    zhenghun = ZhengHun()
    zhenghun.run()
