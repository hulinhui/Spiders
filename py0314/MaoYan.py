import requests
import time
import base64
import math
import random
import hashlib

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 '
                  'Safari/537.36 Edg/112.0.1722.68',
    'Referer': 'https://piaofang.maoyan.com/dashboard',
    'Host': 'piaofang.maoyan.com',
}


def get_maoyan_requsets(url, params):
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response
    except Exception as e:
        print(e)


def get_data(index):
    maoyan_list = ['keys', 'log', 'GET', '171WtxWGj', 'floor', '6586595KrzIYt', "=''", '4INeORR', 'reduce',
                   '303256TgflDf', '1818384COzaid', '2216650lRBaPR', 'error', 'signKey',
                   'A013F70DB97834C0A5492378BD76C53A', 'User-Agent', 'replace', '11nRKPzJ', '7tyVrdd', 'method',
                   '380474DWSxHC', '4045278HuYQWq', '5921330tHaNcD']
    index -= 246
    return maoyan_list[index]


def get_channelId(key):
    maoyan_item = {'baidu': 110001, 'dianping': 6, 'meituan': 3, 'mobile_browser': 0, 'movie': 1, 'moviepro': 40004,
                   'pc_browser': 40009, 'qq': 7, 'qq_browser': 1000030, 'toutiao': 120002, 'uc': 40009, 'wechat': 9,
                   }
    return str(maoyan_item[key])


def base64_data(text):
    return base64.b64encode(text.encode())


def md5_data(text):
    return hashlib.md5(text.encode()).hexdigest()


def get_params():
    params_item = {'method': get_data(248), 'timeStamp': str(int(1000 * time.time())),
                   'User-Agent': base64_data(headers[get_data(261)]).decode(),
                   'index': str(math.floor(1000 * random.random() + 1)), 'channelId': get_channelId('pc_browser'),
                   'sVersion': '2', 'key': get_data(260)}
    str_text = '&'.join([f'{key}={value}' for key, value in params_item.items()])
    item_data = {'orderType': '0', 'uuid': '187fe7c9673c8-06c293af474628-7e57547f-1fa400-187fe7c9673c8',
                 'signKey': md5_data(str_text)}
    list(map(params_item.pop, ['method', 'key']))
    params_item.update(item_data)
    return params_item


def main():
    maoyan_url = 'https://piaofang.maoyan.com/dashboard-ajax/movie?'
    params = get_params()
    response = get_maoyan_requsets(maoyan_url, params)
    if response:
        data = response.json()
        print(len(data['movieList']['list']))
        for movie_info in data['movieList']['list']:
            print(movie_info)


if __name__ == '__main__':
    main()
