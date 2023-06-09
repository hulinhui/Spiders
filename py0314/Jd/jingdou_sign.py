import os

import requests

from py0314.NotifyMessage import send_ding
from py0314.loggingmethod import get_logging


class JdSign(object):
    """docstring for JdSign"""

    def __init__(self):
        super(JdSign, self).__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2011K2C Build/RKQ1.200928.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/045909 Mobile Safari/537.36 MMWEBID/6006 MicroMessenger/8.0.16.2040(0x28001057) Process/tools WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64'
        }
        self.sign_url = 'http://toutiao10.china.com.cn/api/conversation/group/clock/in/h5/sign'
        self.logger = get_logging()  # 获取日志对象
        self.logger.info('微信群京豆签到情况:')
        self.title = '微信群京豆签到情况'

    def get_data(self):
        sign_id = os.environ["wjds_id"] if "wjds_id" in os.environ and os.environ.get(
            "wjds_id") else ''
        unionId = os.environ["wjds_unionId"] if "wjds_unionId" in os.environ and os.environ.get(
            "wjds_unionId") else ''
        name = os.environ["wjds_name"] if "wjds_name" in os.environ and os.environ.get("wjds_name") else ''
        headimgurl = os.environ["wjds_headimgurl"] if "wjds_headimgurl" in os.environ and os.environ.get(
            "wjds_headimgurl") else ''
        return sign_id, unionId, name, headimgurl

    def sign(self, data, wjds_id):
        self.logger.info(f'【{data[2]}】开始打卡【{wjds_id}】....')
        data = {'id': wjds_id, 'unionId': data[1], 'name': data[2], 'headimgurl': data[3]}
        r = requests.post(self.sign_url, headers=self.headers, json=data)
        result = ''
        if r.status_code == 200:
            json_data = r.json()
            if json_data.get('code') == 0 and 'data' in json_data:
                if json_data.get('data').get('status') == 0:
                    result = '【打卡成功√√√】'
                else:
                    result = "【打卡失败×××】失败原因：" + json_data['data']['message']
            else:
                result = "【打卡失败×××】失败原因：" + json_data['message']
        else:
            print('签到接口访问失败')
        return result

    def run(self):
        data = self.get_data()
        for wjds_id in data[0].split('@'):
            result = self.sign(data, wjds_id)
            if result:
                self.logger.info(f'{result}')
            else:
                self.logger.info(f"【{data[2]}-打卡失败×××】失败原因：接口访问失败")
            self.logger.info('#########################################')
        send_ding(self.title, mode=0)


if __name__ == '__main__':
    jd = JdSign()
    jd.run()
