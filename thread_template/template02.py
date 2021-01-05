import queue
import threading

from fake_useragent import UserAgent

headers = {'User-Agent': UserAgent().random}


class Parse(threading.Thread):
    def __init__(self, number, data_list, req_thread):
        super(Parse, self).__init__()
        self.number = number
        self.data_list = data_list
        self.req_thread = req_thread
        self.is_prese = True

    def run(self):
        print(f'启动{self.number}号解析线程')
        while True:
            # 如何判断解析线程的结束体条件
            for t in self.req_thread:
                if t.is_alive():
                    break
            else:
                if self.data_list.qsize() == 0:
                    self.is_prese = False
            if self.is_prese:
                try:
                    data = self.data_list.get()
                except Exception as e:
                    data = None
                if data is not None:
                    self.parse(data)
            else:
                break
        print(f'退出{self.number}号解析线程')

    # 页面解析函数
    def parse(self, data):
        pass


class Crawl(threading.Thread):
    def __init__(self, number, req_list, data_list):
        super(Crawl, self).__init__()
        self.number = number
        self.req_list = req_list
        self.data_list = data_list
        self.headers = headers

    def run(self):
        print(f'启动采集线程{self.number}号')
        while self.req_list.qsize() > 0:
            url = self.req_list.get()
            print(f'{self.number}号线程采集：{url}')
            # time.sleep(random.randint(1,3))
            self.data_list.put('详情页链接数据')


def main():
    concurrent = 3
    conparse = 3

    # 生成请求队列
    req_list = queue.Queue()
    # 生成数据队列
    data_list = queue.Queue()
    # 创建文件对象
    f = open('xxx.json', 'w', encoding='utf-8')

    # 循环生产多个请求url
    for i in range(1, 14):
        base_url = 'https://www.qiushibaike.com/8hr/page/{}/'.format(i)
        req_list.put(base_url)

    # 生成N个采集线程
    req_thread = []
    for i in range(concurrent):
        t = Crawl(i + 1, req_list, data_list)
        t.start()
        req_thread.append(t)

    # 生成N个解析线程
    parse_thread = []
    for i in range(conparse):
        t = Parse(i + 1, data_list, req_thread)
        t.start()
        parse_thread.append(t)

    for t in req_thread:
        t.join()

    for t in parse_thread:
        t.join()

    # 关闭文件对象
    f.close()


if __name__ == '__main__':
    main()
