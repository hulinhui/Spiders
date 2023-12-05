import time

import requests
from lxml import etree
from py0314.NotifyMessage import send_ding
from py0314.loggingmethod import get_logging

title = '163早报'
logger = get_logging()  # 日志
logger.info('163早报信息如下:')


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    try:
        resp = requests.get(url=url, headers=headers)
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        return resp.text
    except Exception as e:
        logger.info(f'接口访问失败,失败原因:{e}')


def parse_html(text):
    if text:
        tree = etree.HTML(text)
        li_list = tree.xpath('//div[@class="tab_content"]/ul/li')
        for li in li_list:
            article_date = li.xpath('./div/div/span/text()')[0]
            today_date = time.strftime('%Y-%m-%d', time.localtime())
            if today_date == article_date.split()[0]:
                article_href = li.xpath('./div/h4/a/@href')[0]
                return article_href
        else:
            logger.info('今日暂无简报信息')


def get_aeticle_info(html):
    if html:
        # print(html)
        tree = etree.HTML(html)
        post_body = tree.xpath('//div[@class="post_body"]')[0]
        if post_body.xpath('./p[1]/@id'):  # 内容可能存在第2个p标签或第3个p便签里
            new_text = '\n'.join(post_body.xpath('./p[1]/text()')[1:])
            return new_text
        elif post_body.xpath('./p[2]/@id'):
            new_text = '\n'.join(post_body.xpath('./p[2]/text()')[1:])
            return new_text
        else:
            new_text = '\n'.join(post_body.xpath('./p[3]/text()')[1:])
            return new_text


def main():
    article_url = 'https://www.163.com/dy/media/T1603594732083.html'
    html = get_html(article_url)
    article_href = parse_html(html)
    if article_href:
        text = get_html(article_href)
        new_text = get_aeticle_info(text)
        logger.info(new_text)
        send_ding(title, mode=0)


if __name__ == '__main__':
    main()
