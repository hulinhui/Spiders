# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         glados.py
# Description:
# Author:       hulinhui779
# Date:      2024/3/16 10:28
# -------------------------------------------------------------------------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: checkin.py(GLaDOS签到)
Author: Hennessey
cron: 40 0 * * *
new Env('GLaDOS签到');
Update: 2023/7/27
"""

import requests
import json
import os
import sys
import time


def get_cookies():
    """判断当前系统，执行对应获取信息的方法"""
    if os.name == 'nt':
        cur_path = os.path.abspath(os.path.dirname(__file__))
        py_path = os.path.abspath(os.path.dirname(cur_path))
        sys.path.append(py_path)
        from py0314.NotifyMessage import read_config
        cookie_text = list(read_config()['GLADOS'].values())
        return real_get_cookies(cookie_text)
    else:
        cookie_text = os.environ.get("GR_COOKIE")
        return real_get_cookies(cookie_text)


# 获取GlaDOS账号Cookie
def real_get_cookies(cookes_text):
    if cookes_text:
        if isinstance(cookes_text, list):
            cookes_text = cookes_text[0]
        if '&' in cookes_text:
            cookies = cookes_text.split('&')
        elif '\n' in cookes_text:
            cookies = cookes_text.split('\n')
        else:
            cookies = [cookes_text]
    else:
        print("未获取到正确的GlaDOS账号Cookie")
        return
    print(f"共获取到{len(cookies)}个GlaDOS账号Cookie")
    return cookies


# 加载通知服务
def load_send():
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/sendNotify.py"):
        try:
            from sendNotify import send
            return send
        except Exception as e:
            print(f"加载通知服务失败：{e}")
            return None
    else:
        print("加载通知服务失败")
        return None


# GlaDOS签到
def get_user_info(response):
    subscribe_endpoint = "update.glados-config.com"
    json_data = response.json() if response else {}
    result = bool(json_data['code']) if json_data and 'code' in json_data else True
    if result:
        return tuple()
    user_item = json_data['data']
    email = user_item['email']
    clash_link = (f"https://{subscribe_endpoint}/clash/{user_item['userId']}/"
                  f"{user_item['code']}/{user_item['port']}/glados.yaml")
    return email, clash_link


def checkin(cookie):
    checkin_url = "https://glados.rocks/api/user/checkin"
    state_url = "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    payload = {
        'token': 'glados.one'
    }
    try:
        checkin = requests.post(checkin_url, headers={
            'cookie': cookie,
            'referer': referer,
            'origin': origin,
            'user-agent': useragent,
            'content-type': 'application/json;charset=UTF-8'}, data=json.dumps(payload))
        state = requests.get(state_url, headers={
            'cookie': cookie,
            'referer': referer,
            'origin': origin,
            'user-agent': useragent})
    except Exception as e:
        print(f"签到失败，请检查网络：{e}")
        return None, None, None

    mess = checkin.json()['message']
    days = checkin.json()['list'][0]['balance'].split('.')[0]
    mail, link = get_user_info(state)
    return mess, days, mail, link


# 执行签到任务
def run_checkin(cookies):
    content_list = []
    for index, cookie in enumerate(cookies, 1):
        ret, remain, email, link = checkin(cookie)
        if ret and email:
            content = f"账号{index}：{email}==>剩余天数：{remain}\n签到结果：{ret}\n订阅地址:{link}"
        else:
            content = f'账号{index}：签到失败，请检查账户信息以及网络环境'
        print(content)
        content_list.append(content)
    contents_str = "\n".join(content_list)
    return contents_str


if __name__ == '__main__':
    title = "GlaDOS签到通知"
    cookie_list = get_cookies()
    if cookie_list:
        content_text = run_checkin(cookie_list)
        # send_notify = load_send()
        # send_notify(title, content_text)
