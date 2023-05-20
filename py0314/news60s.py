import requests
import time
import re
import html
from NotifyMessage import send_pushplus
from loggingmethod import get_logging

logger = get_logging()


def get_href(news_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
    try:
        response = requests.get(news_url, headers=headers)
        response.raise_for_status()
        return response
    except Exception as e:
        logger.info(e)


def get_60s_data():
    news_url = 'https://www.zhihu.com/api/v4/columns/c_1261258401923026944/items'
    response = get_href(news_url)
    if not response:
        logger.info('60s新闻接口访问失败！')
        return
    json_data = response.json()
    if 'data' not in json_data:
        logger.info('60s新闻页面无数据')
        return
    latest_news_update = time.strftime('%Y-%m-%d', time.localtime(json_data['data'][0]['updated']))
    today_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    if today_date != latest_news_update:
        logger.info('今天新闻好像迟到了哦！')
        return
    content_str = re.findall(r'<p.data-pid=.*?>(.*?)</p>', json_data['data'][0]['content'], re.S)
    if not content_str:
        logger.info('60s新闻匹配内容失败')
        return
    content = html.unescape('\n'.join(content_str[1:]))
    logger.info(content)


def main():
    get_60s_data()
    send_pushplus('每天60秒读懂世界')


if __name__ == '__main__':
    main()
