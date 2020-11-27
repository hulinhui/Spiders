import time
from queue import Queue
from threading import Thread


class Demo(Thread):
    def __init__(self, q_list):
        super(Demo, self).__init__()
        self.q = q_list

    def run(self):
        while True:
            q_url = self.q.get()
            try:
                self.parse(q_url)
            finally:
                self.q.task_done()

    def parse(self, url):
        print(f'开始爬取链接：{q_list}')


if __name__ == '__main__':
    start_time = time.time()
    base_url = 'https://www.baidu.com/{}.html'
    url_list = [base_url.format(i) for i in range(1, 31)]
    q_list = Queue()

    for i in range(20):
        worker = Demo(q_list)
        worker.daemon = True
        worker.start()

    for url in url_list:
        q_list.put(url)

    q_list.join()
    print('下载完毕耗时:{:2f}'.format(time.time() - start_time))
