import time
from queue import Queue
from threading import Thread

import requests
from bs4 import BeautifulSoup


class DouTu(Thread):
    def __init__(self, urlqueue):
        super().__init__()
        self.queue = urlqueue
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/94.0.4606.61 Safari/537.36'}
        self.path = 'C:/Users/hulinhui/Pictures/doutula/'

    def get_html(self, url):
        try:
            resp = requests.get(url, headers=self.headers)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding
            return resp
        except Exception as e:
            print(f'页面访问失败：{e}')

    def down_pic(self, title, href):
        file_name = self.path + title.replace('|', '').replace('/', '')
        with open(file_name, 'wb') as f:
            resp = self.get_html(href)
            if resp:
                f.write(resp.content)

    def parse_detail(self, html):
        soup = BeautifulSoup(html.text, 'lxml')
        a_list = soup.select('ul.list-group > li.list-group-item div > a')
        for a in a_list:
            pic_href = a.select_one('img').get('data-original') if len(a.select('img')) < 2 else a.select('img')[1].get(
                'data-original')
            suffix = '.' + pic_href.split('.')[-1] if pic_href.split('.')[-1] != 'null' else '.jpg'
            title = a.select_one('p').get_text()
            pic_title = title.strip()[:5] + suffix if title and pic_href else \
                pic_href.split('/')[-1].replace('null', 'jpg') if pic_href else None
            if pic_href:
                self.down_pic(pic_title, pic_href)

    def run(self) -> None:
        while True:
            url = self.queue.get()
            try:
                print(f'正在爬取页面:{url}')
                html = self.get_html(url)
                self.parse_detail(html)
                print(f'页面:{url}:下载完成！！')
            finally:
                self.queue.task_done()


def main():
    start_time = time.time()
    url_queue = Queue()
    base_url_format = 'https://www.doutula.com/photo/list/?page={}'

    for i in range(2, 11):
        url_queue.put(base_url_format.format(i))

    for i in range(1, 10):
        doutu = DouTu(url_queue)
        doutu.daemon = True
        doutu.start()
    url_queue.join()
    print(f'斗图啦下载总时长{round(time.time() - start_time, 2)}s')


if __name__ == '__main__':
    main()
