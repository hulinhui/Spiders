# 实现卡夫亨氏小程序的签到及兑换功能
import os
import threading
import time

import requests

from py0314.NotifyMessage import send_ding
from py0314.loggingmethod import get_logging


class KaFuHengShi(object):
    """docstring for KaFuHengShi"""

    def __init__(self):
        super(KaFuHengShi, self).__init__()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6307001e)"}
        self.userinfo_url = 'https://fscrm.kraftheinz.net.cn/crm/public/index.php/api/v1/getUserInfo'
        self.sign_url = 'https://fscrm.kraftheinz.net.cn/crm/public/index.php/api/v1/dailySign'
        self.exchange_url = 'https://fscrm.kraftheinz.net.cn/crm/public/index.php/api/v1/exchangeIntegralNew'
        self.share_url = 'https://fscrm.kraftheinz.net.cn/crm/public/index.php/api/v1/recordScoreShare'
        self.logger = get_logging()  # 获取日志对象
        self.title = '卡夫亨氏签到情况'

    def token_data(self):
        kfhs_token = os.environ["kfhs_token"] if "kfhs_token" in os.environ and os.environ.get(
            "kfhs_token") else ''
        kfhs_invite_id = os.environ["kfhs_invite_id"] if "kfhs_invite_id" in os.environ and os.environ.get(
            "kfhs_invite_id") else ''
        kfhs_number = os.environ["kfhs_number"] if "kfhs_number" in os.environ and os.environ.get(
            "kfhs_number") else ''
        return kfhs_token, kfhs_invite_id, int(kfhs_number)

    def get_data(self, url, method='get', data=None):
        if method.lower() == 'get':
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                response.encoding = 'utf-8'
                return response.json()
            except Exception as e:
                return None
        else:
            try:
                response = requests.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                response.encoding = 'utf-8'
                return response.json()
            except Exception as e:
                return None

    def get_userinfo(self):
        json_data = self.get_data(self.userinfo_url)
        if json_data and 'error_code' in json_data:
            if json_data.get('error_code') == 0:
                nickname = json_data['data']['nickname']
                signtimes = json_data['data']['signTimes']
                score = json_data['data']['memberInfo']['totalScore']
                last_sign_time = json_data['data']['serialSign'][0]['updatedAt']
                self.logger.info(f'用户:{nickname},登录成功！')
                self.logger.info(f'用户已连续签到{signtimes}天,当前用户总积分为：{score}!')
                return last_sign_time
            else:
                self.logger.info('获取用户信息失败2')
                exit()
        else:
            self.logger.info('获取用户信息失败1')
            exit()

    def sign(self):
        last_sign_time = self.get_userinfo()
        self.logger.info('签到情况如下:')
        nowtime_str = time.strftime('%Y-%m-%d', time.localtime())
        if last_sign_time:
            last_signtime_str = last_sign_time.split()[0]
            if last_signtime_str != nowtime_str:
                data = self.get_data(self.sign_url, 'post')
                if data and 'error_code' in data:
                    if data['error_code'] == 0:
                        self.logger.info(f"{data['msg']}！！！")
                    else:
                        self.logger.info(f"签到失败原因:{data['msg']}！！！")
                else:
                    self.logger.info('签到接口失败！！！')
            else:
                self.logger.info('今日已签到！！！')
        else:
            self.logger.info('无最后一次签到时间，不执行签到')

    def share(self, invite_id):
        share_data = {'cookbook_id': 206, 'invite_id': invite_id}
        share_result = self.get_data(self.share_url, 'post', share_data)
        if share_data and 'error_code' in share_result:
            self.logger.info(f"分享结果:{share_result['msg']}")
        else:
            self.logger.info('分享结果:分享失败!')

    def exchange_E(self):
        data = {'value': '京东E卡2元', 'phone': '', 'type': '视频卡'}
        json_data = self.get_data(self.exchange_url, 'post', data)
        if json_data and 'error_code' in json_data:
            self.logger.info(f"兑换结果:{json_data['msg']}!!!")
        else:
            self.logger.info(f'兑换失败！！！')

    def run(self):
        kfhs_token, kfhs_invite_id, kfhs_number = self.token_data()
        if kfhs_token and '&' in kfhs_token:
            for token, invite_id in zip(kfhs_token.split('&'), kfhs_invite_id.split('&')):
                self.headers['token'] = token
                self.sign()
                self.share(int(invite_id))
                thred_list = [threading.Thread(target=kfhs.exchange_E) for _ in range(kfhs_number)]
                for t in thred_list:
                    t.start()
                for t in thred_list:
                    t.join()
                self.logger.info('############################')
        else:
            self.logger.info('获取token失败')
        self.logger.info('运行结束！！！')
        send_ding(self.title, mode=0)


if __name__ == '__main__':
    kfhs = KaFuHengShi()
    kfhs.run()
