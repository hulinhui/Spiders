#python实现url编码
from urllib import parse



def url_encode(str):
    str_encode=parse.quote(str)
    return str_encode


def url_decode(str):
    str_decode=parse.unquote(str)
    return str_decode




if __name__ == '__main__':
    str_init='小米11'
    str_encode=url_encode(str_init)
    str_decode=url_decode(str_encode)
    print(str_encode,str_decode)






