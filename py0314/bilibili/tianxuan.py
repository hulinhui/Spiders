# B站天选时刻-自动填写收货地址，兑换奖励
import os

import requests
from py0314.NotifyMessage import send_ding
from py0314.loggingmethod import get_logging

title = 'B站天选时刻'
logger = get_logging()  # 日志
logger.info('B站天选地址情况:')

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44",
           'cookie': os.environ["BZ_Cookie"] if "BZ_Cookie" in os.environ and os.environ.get("BZ_Cookie") else ''}
give_address_url = 'https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/GiveAddressInfo'
record_url = 'https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/AwardRecord?page=1'


def get_data(url, medthod='get', data=None):
    if medthod.lower() == 'get':
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        else:
            return None
    else:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response
        else:
            return None


def filter_data(response):
    if response:
        json_data = response.json()
        if json_data and 'code' in json_data:
            if json_data['code'] == 0:
                data_list = json_data['data']['list']
                ids_list = [data['id'] for data in data_list if
                            not (data['recipient'] and data['phone'] and data['address'])]
                return ids_list
            elif json_data['code'] == -101:
                logger.info('ck失效，请重新登录！')
            else:
                logger.info(f"获取数据失败:{json_data['message']}")
        else:
            logger.info('接口数据获取失败2')
    else:
        logger.info('接口数据获取失败1')


def add_address(data):
    if data:
        logger.info(f'一共有{len(data)}条兑奖信息需要填写！')
        for index, id in enumerate(data, 1):
            data_info = {'id': id,
                         'uid': '',
                         'recipient': 'xxxx',
                         'phone': 'xxxxxx',
                         'address': 'xxxxxxx'
                         }
            response = get_data(give_address_url, 'post', data=data_info)
            if response:
                json_data = response.json()
                logger.info(f"第{index}条录入结果:{json_data['message']}")
            else:
                logger.info(f"第{index}条录入结果:失败")

    else:
        logger.info('暂无新的中奖信息')


def main():
    result = get_data(record_url)
    ids_list = filter_data(result)
    add_address(ids_list)
    send_ding(title, mode=0)


if __name__ == '__main__':
    main()
