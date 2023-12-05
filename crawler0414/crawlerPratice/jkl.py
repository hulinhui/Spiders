# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         jkl
# Description:  爬取京客隆店铺分布信息
# Author:       hlh
# Date:      2023/6/29 16:19
# -------------------------------------------------------------------------------
import pandas as pd
import requests
from crawler0414.crawlerPratice.豆瓣电影 import ua
from lxml import etree


# detail_url='https://www.jkl.com.cn/shopLis.aspx?TypeId=10045'或https://www.jkl.com.cn/shopLis.aspx?current=2&TypeId=10045【多页】

def get_html(url):
    try:
        response = requests.get(url, headers=ua)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        print(e)


def lxml_data(text):
    detail_href = [f"https://www.jkl.com.cn/{href}" for href in
                   etree.HTML(text).xpath('//div[@class="infoLis"]//a/@href')]
    return detail_href


def get_top_html():
    top_url = 'https://www.jkl.com.cn/shop.aspx'
    text = get_html(top_url)
    detail_href = lxml_data(text) if text else None
    return detail_href


def get_detail_page(tree):
    region_name = tree.xpath('//div[@class="infoTit"]/span/strong/text()')[0]
    href_div = tree.xpath('//a[text()="尾页"]/@href')
    page_num = href_div[0].split('&')[0].split('=')[1] if href_div else None
    href_format = href_div[0].replace(page_num, '{}').strip() if page_num else None
    return region_name, page_num, href_format


def parse_detail_data(region, tree):
    shop_list = []
    dd_trees = tree.xpath('//div[@class="shopLis"]/dl/dd')
    for dd_tag in dd_trees:
        shop_item = {'店铺名称': dd_tag.xpath('//span[@class="con01"]/text()')[0] + f'【{region}】',
                     '店铺链接': 'https://www.jkl.com.cn/' + dd_tag.xpath('./a/@href')[0],
                     '经营地址': dd_tag.xpath('//span[@class="con02"]/text()')[0],
                     '电话': dd_tag.xpath('//span[@class="con03"]/text()')[0],
                     '营业时间': dd_tag.xpath('//span[@class="con04"]/text()')[0]
                     }
        shop_list.append(shop_item)
    return shop_list


def get_detail_data(links):
    shop_data = []
    for link in links:
        detail_response = get_html(link)
        # 获取详情页区域及页数
        tree = etree.HTML(detail_response) if detail_response else None
        page_info = get_detail_page(tree) if len(tree) else None
        if not page_info:
            continue
        if page_info[1]:
            for num in range(1, int(page_info[1]) + 1):
                detail_response = get_html(link.split('?')[0] + page_info[2].format(num))
                single_data = parse_detail_data(page_info[0], etree.HTML(detail_response))
                shop_data.extend(single_data)
        else:
            single_data = parse_detail_data(page_info[0], tree)
            shop_data.extend(single_data)
    return shop_data


def main():
    detail_href_list = get_top_html()
    if detail_href_list:
        shop_data = get_detail_data(detail_href_list)
        if shop_data:
            shop_pd = pd.DataFrame(shop_data)
            shop_pd.to_excel('京客隆数据.xlsx', index=False)
        else:
            print('店铺数据为空！')
    else:
        print('获取详情页链接失败!')


if __name__ == '__main__':
    main()
