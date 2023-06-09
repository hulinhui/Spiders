import json

import requests
from bs4 import BeautifulSoup

from py0314.NotifyMessage import send_ding, read_config
from py0314.loggingmethod import get_logging


def get_data(method, url, headers):
    try:
        result_response = requests.request(method=method, url=url, headers=headers)
        result_response.raise_for_status()
        result_response.encoding = 'utf-8'
        return result_response.text
    except Exception as e:
        logger.info(f'接口访问失败,失败原因:{e}')


def config_data(data):
    sign_url = data['HIFINI']['referer']
    title = data['HIFINI'].popitem()[1]
    user_url = data['HIFINI'].popitem()[1]
    headers = dict(data['CURRENCY'], **data['HIFINI'])
    return sign_url, headers, title, user_url


def hifini_sign(sign_url, headers):
    data = get_data('post', sign_url, headers)
    if data:
        result_item = json.loads(data.strip())
        logger.info(result_item['message'])
    else:
        logger.info('签到失败')


def get_sign_info(sign_url, headers):
    text = get_data('get', sign_url, headers)
    if text:
        selector = BeautifulSoup(text, 'lxml')
        td_list = [b.get_text() for b in selector.select('div.card-footer.p-2 td > b')]
        logger.info(f'总签到人数: {td_list[0]}，今日签到： {td_list[1]}，今日第一: {td_list[2]}')
    else:
        logger.info('获取签到信息失败！')


def get_user_info(user_url, headers_data):
    text = get_data('get', user_url, headers_data)
    if text:
        selector = BeautifulSoup(text, 'lxml')
        user_name = selector.select_one('div.card-body.text-center').get_text().strip()
        money = selector.select_one('div.col-md-6 > span:nth-of-type(4) > em').get_text()
        logger.info(f'当前用户:{user_name}，总金币数：{money}')
    else:
        logger.info('获取签到信息失败！')


def main():
    config_items = read_config()
    sign_url, headers_data, title, user_url = config_data(config_items)
    logger.info(f'{title}信息如下:')
    hifini_sign(sign_url, headers_data)
    get_sign_info(sign_url, headers_data)
    get_user_info(user_url, headers_data)
    send_ding(title, mode=0)


if __name__ == '__main__':
    logger = get_logging()  # 日志
    main()
