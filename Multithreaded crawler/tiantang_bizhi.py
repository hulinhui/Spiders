##此网站下载易出现429，暂时无解
##列表页链接：https://www.ivsky.com/bizhi/dongman_1920x1080/index_2.html
##图片真实下载地址:https://img-picdown.ivsky.com/img/bizhi/pic/201909/17/guimiezhiren.jpg?
##https://img.ivsky.com/img/bizhi/t/201909/17/guimiezhiren.jpg
import time, os, re
from queue import Queue
import requests
from bs4 import BeautifulSoup
from threading import Thread

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}


class TianTangPic(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.domain = 'https://www.ivsky.com'
        self.down_url = 'https://img-picdown.ivsky.com'
        self.path = 'C:/Users/hulinhui/Pictures/tiantang_pic/'

    def get_html(self, url):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        else:
            return ''

    def parse_detail_html(self, html):
        if html:
            img_list = []
            soup = BeautifulSoup(html.text, 'lxml')
            li_list = soup.select('ul.pli > li')
            for li in li_list:
                link_url = li.select_one('div.il_img > a > img').get('src')
                img_url = link_url.split('com')[1].replace('t', 'pic', 2)
                img_list.append(img_url)
            if img_list:
                return img_list
        else:
            print('获取detail页失败')

    def down_pic(self, filename, img_list):
        filename = self.path + filename
        if not os.path.exists(filename): os.mkdir(filename)
        for img_url in img_list:
            print(img_url)
            filepath = filename + '/' + img_url.split('/')[-1]
            with open(filepath, 'wb') as f:
                response = self.get_html(self.down_url + img_url)
                if response:
                    f.write(response.content)
                else:
                    print(response.status_code)

    def parse_html(self, html):
        if html:
            select_soup = BeautifulSoup(html.text, 'lxml')
            li_list = select_soup.select('ul.ali > li')
            for li in li_list:
                picfilename = re.sub('[/:·]', '', li.select_one('div.il_img > a').get('title'))
                detail_url = self.domain + li.select_one('div.il_img > a').get('href')
                detail_html = self.get_html(detail_url)
                img_list = self.parse_detail_html(detail_html)
                self.down_pic(picfilename, img_list)
                print(f'{picfilename}：下载完成！！')
        else:
            print('html列表页获取失败')

    def run(self):
        while True:
            url = self.queue.get()
            try:
                print(f'正在爬取页面:{url}')
                html = self.get_html(url)
                self.parse_html(html)
            finally:
                self.queue.task_done()


def main():
    start_time = time.time()
    base_url = 'https://www.ivsky.com/bizhi/dongman_1920x1080/index_{}.html'
    base_url_list = [base_url.format(i) if i != 1 else base_url.split('in')[0] for i in range(1, 2)]
    # print(base_url_list)
    url_queue = Queue()

    for i in range(1, 2):
        ttbz = TianTangPic(url_queue)
        ttbz.daemon = True
        ttbz.start()

    for url in base_url_list:
        url_queue.put(url)

    url_queue.join()
    print(f'下载完毕，耗时{round(time.time() - start_time, 2)}s')


if __name__ == '__main__':
    main()
