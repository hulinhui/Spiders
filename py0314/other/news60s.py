import requests
from py0314.loggingmethod import get_logging
from py0314.NotifyMessage import send_pushplus
from py0314.FormatHeaders import get_format_headers, headers_gw
from bs4 import BeautifulSoup
import time


class New_60s:
    def __init__(self):
        self.logger = get_logging()
        self.headers = get_format_headers(headers_gw)

    def get_response(self, url, method='GET', data=None):
        try:
            response = requests.request(method=method, url=url, headers=self.headers, data=data)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response
        except Exception as e:
            self.logger.info(f'【早报网】:请求失败，原因:{e}!')

    @staticmethod
    def parse_home_html(response):
        text = response.text if response else ''
        soup = BeautifulSoup(text, 'lxml')
        item_list = [{'href': _.select_one('header > h2 > a').get('href'),
                      'date_time': _.select_one('p > span:nth-of-type(1)').get_text()} for _ in
                     soup.select('article.excerpt')] if soup else []
        return item_list

    @staticmethod
    def parse_detail_html(response):
        text = response.text if response else ''
        soup = BeautifulSoup(text, 'lxml')
        text_list = [_.get_text() for _ in soup.select('article.article-content > p > strong')] if soup else []
        span_list = [_.get_text() for _ in soup.select('article.article-content > p > span')] if soup else []
        text_list.extend(span_list)
        message_text = '\n'.join(text_list) if text_list else ''
        return message_text

    def get_top_news(self, new_date):
        home_url = 'https://www.qqorw.cn/?page=1'
        response = self.get_response(url=home_url)
        item_list = self.parse_home_html(response)
        url_list = [item.get('href') for item in item_list if
                    item.get('date_time').find(new_date) > -1] if item_list else item_list
        return url_list

    def run(self):
        new_date = time.strftime('%Y-%m-%d', time.localtime())
        url_list = self.get_top_news(new_date)
        if not url_list:
            self.logger.info(f'【早报网】:{new_date}-新闻好像迟到了哦!')
            return
        response = self.get_response(*url_list)
        message = self.parse_detail_html(response)
        if not message:
            self.logger.info('【早报网】:获取详情页新闻失败!')
            return
        self.logger.info(message)
        send_pushplus('早报网新闻推送')


if __name__ == '__main__':
    new = New_60s()
    new.run()
