import os
import time

import requests
from py0314.NotifyMessage import send_ding
from py0314.loggingmethod import get_logging


class HeCaiYun(object):
    """docstring for HeCaiYun"""

    def __init__(self):
        super(HeCaiYun, self).__init__()
        self.sign_url = 'https://caiyun.feixin.10086.cn:7071/portal/ajax/common/wechatSign.action'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2011K2C Build/RKQ1.200928.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/045909 Mobile Safari/537.36 MMWEBID/9555 MicroMessenger/8.0.16.2040(0x28001057) Process/tools WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64'}
        self.logger = get_logging()
        self.logger.info('和彩云签到情况如下:')
        self.title = '和彩云'

    def get_cookies(self):
        cookies = ''
        cookie_str = os.environ["hcy_cookie"] if "hcy_cookie" in os.environ and os.environ.get(
            "hcy_cookie") else 'SESSION=Zjk3NmYyZDYtNDQ4Ny00NTdjLWEzMzItMTQ2ZTk4ZjNkMGE2; WAPJSESSIONID=f976f2d6-4487-457c-a332-146e98f3d0a6; bc_mo="MTc2MjAzODczMzk="; bc_to="ZzVONWJmRER8MXxSQ1N8MTY0MjU4MTk2OTA3MXxsVG1KRXRweV91VTBLcmNBaC5wOWVJWlAucWlZQ185aVVvS1BCU2ZUMFZwbkJHLlJWUk8wa0t3cGdGS1doRlVLV3NsblZKRkJVamJyRFR1TjBENElmWGdOdGtjUXVrN3FpR2dtX2taUTBFRTdCQjQ0blVWSFFmZnZIdHNCUzdQSWxfWWYwaDFFeTdpY29lMkNPbElreGZYU0ZiaTVuSi5XSDJ6Q19QaGZBNGMt"; bc_ps="MTA1NzgyMDg2MA=="; sajssdk_2015_cross_new_user=1; SESSION=Zjk3NmYyZDYtNDQ4Ny00NTdjLWEzMzItMTQ2ZTk4ZjNkMGE2; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217dd704a5fc448-0955fa4714e05a-50142617-376980-17dd704a5fd494%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22phoneNumber%22%3A%2217620387339%22%7D%2C%22%24device_id%22%3A%2217dd704a5fc448-0955fa4714e05a-50142617-376980-17dd704a5fd494%22%7D'
        if cookie_str and '@' in cookie_str:
            cookie_list = cookie_str.split('@')
            cookies = cookie_list
        elif cookie_str and '@' not in cookie_str:
            cookies = cookie_str
        else:
            self.logger.info('无法获取到cookies值')
        if isinstance(cookies, list):
            for index, cookie in enumerate(cookies, 1):
                self.logger.info(f'第{index}个账号签到信息：')
                self.sign(cookie)
                self.logger.info('##################')
        else:
            self.sign(cookies)
            self.logger.info('##################')
        send_ding(self.title, mode=0)

    def sign(self, cookie):
        self.headers['Cookie'] = cookie
        data = {'op': 'sign'}
        resp = requests.post(url=self.sign_url, headers=self.headers, data=data)
        if resp.status_code == 200:
            json_data = resp.json()
            if 'code' in json_data and json_data.get('code') == 10000:
                cloud = json_data['result']['cloud']
                allCloud = json_data['result']['allCloud']
                highCloud = json_data['result']['highCloud']
                self.logger.info(f'签到成功:本次获取{cloud}积分,总共{allCloud}积分,还可以获取{highCloud}积分')
                self.userinfo()
            elif 'code' in json_data and json_data.get('code') == 10001:
                self.logger.info(f"签到成功:{json_data['msg']}")
                self.userinfo()
            else:
                self.logger.info(f'签到失败,失败原因:{json_data["msg"]}')
        else:
            self.logger.info('接口访问失败')

    def userinfo(self):
        resp = requests.post(url=self.sign_url, headers=self.headers, data={'op': 'getUserInfo'})
        if resp.status_code == 200:
            json_data = resp.json()
            if 'code' in json_data and json_data.get('code') == 10000:
                if 'result' in json_data:
                    allCloud = json_data['result']['allCloud']
                    sign_info_list = json_data['result']['weekSign']
                    self.logger.info(f'当前用户总共积分:{allCloud};历史签到记录如下：')
                    for sign_info in sign_info_list:
                        sign_date = time.strftime("%Y年%m月%d日", time.localtime(int(str(sign_info['insertTime'])[:-3])))
                        sign_cloud = sign_info['cloud']
                        sign_weekday = str(sign_info['weekDay'])
                        self.logger.info(f'【{sign_date}-周{sign_weekday}】,签到获取积分:{sign_cloud}')
                else:
                    self.logger.info('个人信息数据中不存在result数据')
            elif 'code' in json_data and json_data.get('code') == 90001:
                self.logger.info(json_data['msg'])
            else:
                self.logger.info('获取个人信息失败')
        else:
            self.logger.info('个人信息接口访问失败')


if __name__ == '__main__':
    hecaiyun = HeCaiYun()
    hecaiyun.get_cookies()
