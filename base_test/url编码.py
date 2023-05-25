# python实现url编码
from urllib import parse


def url_encode(str):
    str_encode = parse.quote(str)
    return str_encode


def url_decode(str):
    str_decode = parse.unquote(str)
    return str_decode


if __name__ == '__main__':
    str_init = '小米11'
    str_encode = url_encode(str_init)
    str2 = '%E5%8C%97%E4%BA%AC%7C101010100%7C'
    str_decode = url_decode(str2)
    print(str_encode, str_decode)
