from queue import Queue
from threading import Thread
import requests
import time
import os
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/94.0.4606.61 Safari/537.36'}


class DouTuW(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.domain = 'https://www.doutuwang.com/'
        self.path = r'C:/Users/hlh/OneDrive/Pictures/pictures/dutuwang/'

    def run(self):
        while True:
            q_url = self.queue.get()
            try:
                self.parse(q_url)
            finally:
                self.queue.task_done()

    @staticmethod
    def get_href(request_url):
        try:
            response = requests.get(request_url, headers=headers)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response
        except Exception as e:
            print(e)

    def parse(self, requests_url):
        print(f'正在爬取:{requests_url}')
        response_text = requests.get(requests_url, headers=headers)
        soup_obj = BeautifulSoup(response_text.text, 'lxml')
        img_list = soup_obj.select('div.wapper > li img')
        # print(img_list,len(img_list))
        if not img_list:
            print('获取图片链接列表失败！')
            return
        for data in img_list:
            img_url = data.get('src')
            img_name = data.get('alt')
            self.down_pic(img_url, img_name)

    def down_pic(self, img_url, img_name):
        suffix = '.' + img_url.split('.')[-1]
        filepath = os.path.join(self.path, img_name) if img_name.endswith(suffix) else os.path.join(self.path,
                                                                                                    img_name + suffix)
        content = self.get_href(img_url).content
        with open(filepath, 'wb') as fp:
            fp.write(content)
            print(f'{img_name}下载成功!')


if __name__ == '__main__':
    start_time = time.time()
    base_url: str = 'https://www.doutuwang.com/category/zuixin{}'
    url_list = [base_url.format(f'/page/{i}') if i != 1 else base_url.format('') for i in range(1, 6)]
    q_page = Queue()

    for i in range(1, 6):
        worker = DouTuW(q_page)
        worker.daemon = True
        worker.start()

    for url in url_list:
        q_page.put(url)

    q_page.join()

    print('下载完毕,耗时:{}s'.format(round(time.time() - start_time, 2)))
