from queue import Queue
from threading import Thread

import requests
import time
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}


class Linux_Pic(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.domain = 'http://www.linuxidc.com'
        self.path = 'C:/Users/hulinhui/Pictures/linux_pic/'

    def run(self):
        while True:
            q_url = self.queue.get()
            try:
                self.parse(q_url)
            finally:
                self.queue.task_done()

    def parse(self, url):
        print(f'正在爬取:{url}')
        seletor = '#dlNews > tr > td > a'  # 获取详情页地址
        seletor2 = '#content > p img'  # 获取图片地址
        data_list = self.get_seletor_data(url, seletor)
        if data_list:
            for data in data_list:
                detail_url = self.domain + data.get('href').split('..')[-1]
                img_list = self.get_seletor_data(detail_url, seletor2)
                if img_list:
                    for img in img_list:
                        if img.get('src'):
                            pic_url = self.domain + img.get('src').split('..')[-1]
                            title = img.get('alt') if img.get('alt') else pic_url.split('/')[-1]
                            self.down_pic(pic_url, title)
                else:
                    print(f'获取图片链接{detail_url}失败')
        else:
            print(f'获取详情页{url}数据失败')

    def down_pic(self, url, title):
        filepath = self.path + title + '.' + url.split('.')[-1]
        if url.split('.')[-1] in title:
            filepath = self.path + title
        content = requests.get(url, headers=headers).content
        with open(filepath, 'wb') as fp:
            fp.write(content)
            print(f'{title}下载成功!')

    def get_seletor_data(self, url, seletor):
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content.decode(), 'lxml')
            data_list = soup.select(seletor)
            if data_list:
                return data_list
            else:
                seletor3 = '#content > center img'
                data_list = self.get_seletor_data(url, seletor3)
                if data_list:
                    return data_list
                else:
                    return None

        else:
            print(f"相应状态码：{resp.status_code}")
            return None


if __name__ == '__main__':
    start_time = time.time()
    base_url = 'http://www.linuxidc.com/Linuxwallpaper/index{}.htm'
    url_list = [base_url.format(f'p{i}') if i != 1 else base_url.format('') for i in range(1, 6)]
    q_page = Queue()

    for i in range(6):
        worker = Linux_Pic(q_page)
        worker.daemon = True
        worker.start()

    for url in url_list:
        q_page.put(url)

    q_page.join()

    print('下载完毕,耗时:{}s'.format(round(time.time() - start_time, 2)))
