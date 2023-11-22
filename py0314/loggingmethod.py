import logging
import os


def get_logging():
    # 1、创建一个logger
    logger = logging.getLogger()
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        # 2、创建一个handler，用于写入日志文件
        fh = logging.FileHandler(os.path.join(os.path.dirname(__file__), 'log.txt'), mode='w', encoding='utf-8')
        # 3、定义handler输出格式
        fh.setFormatter(logging.Formatter('%(message)s'))
        # 4、将logger添加到handler
        logger.addHandler(fh)

        # 1、创建一个handler，用于写入日志文件
        ch = logging.StreamHandler()
        # 2、定义handler输出格式
        ch.setFormatter(logging.Formatter('[%(asctime)s]:%(levelname)s:%(message)s'))
        # 3、将logger添加到handler
        logger.addHandler(ch)

    return logger


if __name__ == '__main__':
    get_logging()
