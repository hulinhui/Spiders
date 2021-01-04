# -*- coding: utf-8 -*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         world_spiders
# Description:  
# Author:       hlh
# Date:      2021/1/4 23:09
#-------------------------------------------------------------------------------

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


class World_Spider():
    def __init__(self):
        self.start_url='http://cn.flagbox.net/'
        self.headers={'User-Agent':UserAgent().random}
        self.filepath=''
        self.data_list=[]

    def get_html(self,url):
        try:
            response=requests.get(url,headers=self.headers)
            response.raise_for_status()
            response.encoding=response.apparent_encoding
            return response.text
        except:
            print('获取数据失败')

    def get_url(self,text,selector):
        soup=BeautifulSoup(text,'lxml')
        link_list=soup.select(selector)
        url_list=['http://cn.flagbox.net/'+url.get('href') for url in link_list]
        return url_list

    def get_country_info(self,text):
        soup=BeautifulSoup(text,'lxml')
        table_selector=soup.select_one('div#page-bg > table tr > td:nth-of-type(1) > table table:nth-of-type(2)')
        item={}
        try:
            country=table_selector.select('tr:nth-of-type(1) > td:nth-of-type(2)')
            item['国家']=country[0].get_text() if len(country) else ''

            population=table_selector.select('tr:nth-of-type(2) > td:nth-of-type(2)')
            item['人口'] = population[0].get_text() if len(country) else ''

            area=table_selector.select('tr:nth-of-type(3) > td:nth-of-type(2)')
            item['面积'] = area[0].get_text() if len(country) else ''

            capital=table_selector.select('tr:nth-of-type(4) > td:nth-of-type(2)')
            item['首都'] = capital[0].get_text() if len(country) else ''

            position=table_selector.select('tr:nth-of-type(5) > td:nth-of-type(2)')
            item['位置'] = position[0].get_text() if len(country) else ''

            Telephone_code = table_selector.select('tr:nth-of-type(6) > td:nth-of-type(2)')
            item['电话代码'] = Telephone_code[0].get_text() if len(country) else ''

            currency = table_selector.select('tr:nth-of-type(9) > td:nth-of-type(2)')
            item['货币名称'] = currency[0].get_text() if len(country) else ''

            language = table_selector.select('tr:nth-of-type(14) > td:nth-of-type(2)')
            item['语言'] = language[0].get_text() if len(country) else ''
            return item
        except Exception as e:
            print(e)


    def download_data(self,item):
        pass


    def get_imglink(self,text):
        pass

    def download_imglink(self,url):
        pass


    def run(self):
        response=self.get_html(self.start_url)
        selector1='div#page-bg > table tr > td:nth-of-type(2) > ul > li > a'
        selector2='tr > td > a:nth-of-type(2)'
        data_list=self.get_url(response,selector1)
        for first_url in data_list:
            first_html=self.get_html(first_url)
            second_urllist=self.get_url(first_html,selector2)
            for second_url in second_urllist:
                second_html=self.get_html(second_url)
                item_data=self.get_country_info(second_html)
                img_url=self.get_imglink(second_html)
                self.download_data(item_data)
                self.download_imglink(img_url)






if __name__=='__main__':
    world_data=World_Spider()
    world_data.run()