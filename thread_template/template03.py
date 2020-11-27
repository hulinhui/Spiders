import multiprocessing
import os


class ProcessClass(multiprocessing.Process):
    def __init__(self, queue):
        super(ProcessClass, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                break
            else:
                item = self.queue.get()
                self.parse(item)

    def parse(self, item):
        print(f'[{os.getpid()}]号进程：{item}')
        pass


def main():
    # 队列必须使用多线程队列，使用queue模块报错
    queue = multiprocessing.Queue()
    for i in range(20):
        queue.put(i)

    process_list = []
    process_num = 4
    for i in range(process_num):
        p = ProcessClass(queue)
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()


if __name__ == '__main__':
    main()
