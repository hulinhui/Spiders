# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         J51_job
# Description:  
# Author:       hlh
# Date:      2023/5/27 14:50
# -------------------------------------------------------------------------------
import hmac
import json
import math
import re
import time
from hashlib import sha256
from urllib.parse import quote

import execjs
import requests
from bs4 import BeautifulSoup

from py0314.FormatHeaders import get_format_headers, headers_one, update_cookies

headers = get_format_headers(headers_one)


def get_encrypt_timestamp(detail_url):
    value = run_51_js('51job_02.js', 'encrypt_value', detail_url)
    params_value = f'{value}|{0}|{math.floor(time.time() * 1000)}'
    timestamp_value = run_51_js('51job_02.js', 'encrypt_timestamp', params_value)
    return timestamp_value


def run_51_js(filename, funcname, argname):
    with open(filename, 'r', encoding='utf-8') as f:
        js_text = f.read()
    js_obj = execjs.compile(js_text)
    return js_obj.call(funcname, argname)


def get_response(real_detail_url, method='get', headers=headers):
    try:
        detail_response = requests.request(method=method, url=real_detail_url, headers=headers, allow_redirects=False)
        detail_response.raise_for_status()
        return detail_response
    except Exception as e:
        print(e)


def parser_detail(html):
    job_item = {}
    if not html:
        return job_item
    try:
        text = html.content.decode('gbk').replace('&nbsp;', '')
    except Exception:
        text = html.content.decode('utf-8')
    soup = BeautifulSoup(text, 'lxml')
    base_info_divs = soup.select_one('div.cn')
    job_item['job_name'] = base_info_divs.select_one('h1').text
    job_item['job_salary'] = base_info_divs.select_one('strong').text
    job_item['job_type'] = base_info_divs.select_one('p').get('title')
    job_item['job_tag'] = '|'.join([tag.text for tag in base_info_divs.select('div.t1 > span')])
    job_info_divs = soup.select_one('div.tCompany_main > div:nth-of-type(1) > div')
    job_info_list = re.split('\r\s+\n', job_info_divs.text.strip())
    job_item['job_info'] = job_info_list[0] if len(job_info_list) >= 1 else ''
    job_keyword = re.findall('<a.*?welfare=">(.*?)</a>', str(job_info_divs))
    job_item['describe'] = ','.join(job_info_list[-1].split('\n')[:-1]) if len(job_info_list) >= 2 else ''
    job_item['job_keywords'] = ','.join([key for key in job_keyword]) if job_keyword else ''
    job_item['company_address'] = \
        soup.select_one('div.tCompany_main > div:nth-of-type(2) > div > p').text.strip().split('：')[1]
    job_item['company_name'] = soup.select_one('div.tCompany_sidebar > div:nth-of-type(1) > div.com_msg p').text
    job_item['company_tag'] = '|'.join(
        [tag.get('title') for tag in soup.select('div.tCompany_sidebar > div:nth-of-type(1) > div.com_tag > p')])
    return job_item


def get_detail_data():
    for job_id in job_id_list:
        detail_url = f'https://jobs.51job.com/shenzhen/{job_id}.html?s=sou_sou_soulb&t=0_0&req={req}'
        timestamp__1258 = get_encrypt_timestamp(detail_url)
        real_detail_url = detail_url + f'&timestamp__1258={timestamp__1258}'

        html = get_response(real_detail_url)
        info_items = parser_detail(html)
        print(info_items)


def get_sign(value):
    key = 'abfc8f9dcf8c3f3d8aa294ac5f2cf2cc7767e5592590f39c3f503271dd68562b'
    sign = hmac.new(key.encode(), value.encode(), digestmod=sha256).hexdigest()
    return sign


def get_list_data(url):
    response = get_response(url)
    if not response:
        print('获取列表数据失败！')
        return
    text = response.text
    # json数据
    if not text.startswith('<html>'):
        return json.loads(text)

    # html加密页面
    value = re.search("var arg1='(.*?)';", text)
    if value:
        acw_v2 = run_51_js('51job_01.js', '_0x4818', value.group(1))
        update_cookies(headers, acw_v2)
        data = get_response(url)
        if not data:
            return
        return data.json()
    else:
        print('获取页面的arg1值失败！')
        return


def update_headers(url, userinfo):
    accountId = userinfo['accountId']
    headers_info = {'Host': 'we.51job.com', 'account-Id': accountId, 'partner': userinfo['partner'],
                    'uuid': userinfo['uuid'],
                    'user-token': userinfo['token'], 'From-Domain': '51job_web',
                    'Sign': get_sign(url.split('com/')[1])}
    headers.update(headers_info)


def result_data(data):
    if not data:
        return ()
    if 'status' not in data and data.get('status') != '1':
        return ()
    requestId = data['resultbody']['requestId']
    jobId_list = [item['jobId'] for item in data['resultbody']['job']['items']]
    return requestId, jobId_list


def get_job_list(page_num, keyword, userinfo, rid=''):
    if userinfo:
        timestamps = int(time.time())
        job_list_url = f"https://we.51job.com/api/job/search-pc?api_key=51job&timestamp={timestamps}&keyword={quote(keyword)}&searchType=2&function=&industry=&jobArea=040000&jobArea2=&landmark=&metro=&salary=&workYear=&degree=&companyType=&companySize=&jobType=&issueDate=&sortType=0&pageNum={page_num}&requestId={rid}&pageSize=20&source=1&accountId={userinfo['accountId']}&pageCode=sou%7Csou%7Csoulb"
        update_headers(job_list_url, userinfo)
        data = get_list_data(job_list_url)
        return result_data(data)
    else:
        print('用户信息获取失败，无法获取列表数据！')


def get_job_token():
    token_url = 'https://oauth.51job.com/ajax/get_token.php?fromdomain=51job_web'
    response = get_response(token_url, 'post')
    if not response:
        return None
    token_data = response.json()
    if not token_data.get('status') == "1":
        return None
    return token_data['resultBody']


if __name__ == '__main__':
    token_info = get_job_token()
    req, job_id_list = get_job_list(2, 'python爬虫', token_info)
    headers['Host'] = 'jobs.51job.com'
    if req and job_id_list:
        get_detail_data()
    else:
        print('获取详情页id失败！')
