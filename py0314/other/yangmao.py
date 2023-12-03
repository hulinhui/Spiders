import time

import requests
from lxml import etree

from py0314.NotifyMessage import send_ding
from py0314.loggingmethod import get_logging

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4613.0 Safari/537.36 Edg/95.0.1000.0'}

logger = get_logging()


def get_html(url):
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        print(f'访问失败，失败原因：{e}')


def parse_html(html):
    logger.info('有奖之家羊毛信息如下:')
    article_text = ''
    tree = etree.HTML(html)
    article_list = tree.xpath('//div[@class="content"]/article')
    today = time.strftime('%Y-%m-%d', time.localtime())
    tag_list = ['免费领红包', '有奖活动网', 'QQ活动网', '微信活动网', '视频会员优惠']
    i = 1
    for article in article_list:
        createtime = article.xpath('./p/time/text()')[0].strip()
        tag_text = article.xpath('./header/a/text()')[0].strip()
        print(createtime, tag_text)
        if createtime == today and tag_text in tag_list:
            article_title = article.xpath('./header/h2/a/text()')[0]
            article_link = article.xpath('./a/@href')[0]
            article_text += f'{i}、【{tag_text}】{article_title}-->查看详情：{article_link}\n'
            i += 1
    if article_text:
        return article_text
    else:
        article_text += '今日暂无羊毛信息更新'
        return article_text


def main():
    base_url = 'https://www.youjiangzhijia.com/'
    html = get_html(base_url)
    info_message = parse_html(html)
    logger.info(info_message)
    # send_ding('有奖之家资讯信息', mode=1)


if __name__ == '__main__':
    main()
