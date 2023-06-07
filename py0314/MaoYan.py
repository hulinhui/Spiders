import re

import requests
import time
import base64
import math
import random
import hashlib
from fontTools.ttLib import TTFont
from PIL import ImageFont, Image, ImageDraw
from io import BytesIO
from cnocr import CnOcr

from fontTools.ttLib.woff2 import decompress

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 '
                  'Safari/537.36 Edg/112.0.1722.68',
    'Referer': 'https://piaofang.maoyan.com/dashboard',
    'Host': 'piaofang.maoyan.com',
    'Origin': 'https://piaofang.maoyan.com',
    'Sec-Fetch-Dest': 'font'
}


def get_maoyan_requsets(url, params=None):
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


def get_font_data(font_url=None):
    if not font_url:
        font_filename = 'e3dfe524.woff'
        xml_filename = 'e3dfe524.xml'
    else:
        font_filename = font_url.split('/')[-1]
        xml_filename = font_filename.split('.')[0] + '.xml'
        headers['Host'] = 's3plus.meituan.net'
        f = open(font_filename, 'wb')
        font_resp = get_maoyan_requsets(font_url)
        f.write(font_resp.content)
        f.close()
    font = TTFont(font_filename)
    font.saveXML(xml_filename)
    font_uni_list = font.getGlyphOrder()[2:]
    return font_uni_list, font


def get_ttf_font(font_url=None):
    if not font_url:
        font_filename = 'e3dfe524.woff'
    else:
        font_filename = font_url.split('/')[-1]
        headers['Host'] = 's3plus.meituan.net'
        f = open(font_filename, 'wb')
        font_resp = get_maoyan_requsets(font_url)
        f.write(font_resp.content)
        f.close()
    ttf_filename = font_filename.split('.')[0] + '.ttf'
    decompress(font_filename, ttf_filename)
    return TTFont(ttf_filename), ttf_filename


def get_maoyan_dict(font_list):
    number_list = [9, 2, 4, 1, 5, 3, 6, 8, 0, 7]
    dict = {'uniEB19': 9, 'uniE3EC': 2, 'uniF7D2': 4, 'uniED30': 1, 'uniF3E8': 5, 'uniF11C': 3, 'uniEA60': 6,
            'uniEF28': 8,
            'uniEA6F': 0, 'uniE3DF': 7}
    return dict(zip(font_list, number_list))


def get_font_img(ttf_obj):
    img_size = 512
    font_img = ImageFont.truetype(ttf_obj[1], img_size)
    for cmap_code, glyph_name in ttf_obj[0].getBestCmap().items():
        img = Image.new('1', (img_size, img_size), 255)
        draw = ImageDraw.Draw(img)
        txt = chr(cmap_code)
        x, y = draw.textsize(txt, font=font_img)
        draw.text(((img_size - x) // 2, (img_size - y) // 2), txt, font=font_img, fill=0)
        bytes_io = BytesIO()
        img.save(bytes_io, format="PNG")
        ocr=CnOcr()
        word = ocr.ocr_for_single_line(bytes_io.getvalue())  # 识别字体
        print(cmap_code, glyph_name, word)


def get_maoyan_data(response):
    if not response:
        return {}
    data = response.json()
    font_url = 'https:' + re.search(r',url\("(.*)"\);', data['fontStyle']).group(1)
    ttf_obj = get_ttf_font()
    get_font_img(ttf_obj)


def main():
    maoyan_url = 'https://piaofang.maoyan.com/dashboard-ajax/movie?'
    params = get_params()
    response = get_maoyan_requsets(maoyan_url, params)
    local_font_tuple = get_font_data()
    local_font_dict = get_maoyan_dict(local_font_tuple[0])
    print(local_font_dict)
    get_maoyan_data(response)


if __name__ == '__main__':
    main()
