import base64
import codecs
import json
import random
import string
from math import ceil
from multiprocessing import Pool

import requests
from Crypto.Cipher import AES
from fake_useragent import UserAgent


class WangyiSpider():
    def __init__(self, song_id, song_name):
        self.song_id = song_id
        self.song_name = song_name
        self.headers = {"User-Agent": UserAgent().random}
        self.url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
        # 三个固定参数
        # bkk4o(["流泪", "强"])的值
        self.second_param = "010001"
        # bkk4o(YS0x.md)的值
        self.third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        # bkk4o(["爱心", "女孩", "惊恐", "大笑"])的值
        self.fourth_param = "0CoJUm6Qyw8W8jud"

    def create_random_16(self, randomsize=16):
        str_list = [random.choice(string.ascii_letters + string.digits) for _ in range(randomsize)]
        random_str = ''.join(str_list)
        return random_str

    def aesEncrypt(self, a, b):
        # 偏移量
        iv = '0102030405060708'
        # 文本[补齐文本长度]
        BS = AES.block_size  # 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - (len(s) % BS))
        encryptor = AES.new(bytearray(b, 'utf-8'), AES.MODE_CBC, bytearray(iv, 'utf-8'))
        ciphertext = encryptor.encrypt(bytearray(pad(a), 'utf-8'))
        ciphertext = base64.b64encode(ciphertext)
        ciphertext=ciphertext.decode('utf-8')
        return ciphertext

    def rsa_encrypt(self, i, e, f):
        # 随机字符串逆序排列
        text = i[::-1]
        # 将随机字符串转换成byte类型数据
        text = bytes(text, 'utf-8')
        # RSA加密
        sec_key = int(codecs.encode(text, encoding='hex'), 16) ** int(e, 16) % int(f, 16)
        # 返回结果
        return format(sec_key, 'x').zfill(256)

    # 获取请求参数
    def get_params(self,page=4):
        self.frist_param = '{"csrf_token": "","cursor": "-1","offset": "0","orderType": "1","pageNo": %s,"pageSize": "20","threadId": "R_SO_4_%s"}' % (
        page,self.song_id)
        # print(self.frist_param)
        # 生成长度为16的随机字符串
        text = self.create_random_16()
        # 第一次AES加密
        encText = self.aesEncrypt(self.frist_param, self.fourth_param)
        # 第二次AES加密之后得到params的值
        encText = self.aesEncrypt(encText, text)
        # RSA加密之后得到encSecKey的值
        encSecKey = self.rsa_encrypt(text, self.second_param, self.third_param)
        return encText, encSecKey

    # 打印评论数据
    def get_comment(self, page):
        params, encSecKey = self.get_params(page)
        data = {'params': params, 'encSecKey': encSecKey}
        resp_json = requests.post(self.url, headers=self.headers, data=data).json()
        if resp_json and resp_json['code'] == 200:
            print("正在爬取第{}页的评论".format(page))
            commtent_list=resp_json['data']['comments']
            with open(f"{self.song_name}.json",'a',encoding='utf-8') as f:
                for data in commtent_list:
                    item_data={}
                    item_data['nickname']=data['user']['nickname']
                    item_data['userId'] = data['user']['userId']
                    item_data['avatarUrl'] = data['user']['avatarUrl']
                    item_data['vipType'] = data['user']['vipType']
                    item_data['content'] = data['content'].replace('\n','')
                    print(item_data)
                    f.write(json.dumps(item_data,ensure_ascii=False)+'\n')
            print(f"{self.song_name}:第{page}页的评论下载成功")
        else:
            print(f"爬取页面{page}数据失败")

    def run(self):
        #创建进程池
        p=Pool(processes=4)
        # 1、获取params,encSecKey参数
        params, encSecKey = self.get_params()
        # 2、构造data
        data = {'params': params, 'encSecKey': encSecKey}
        # 请求评论接口
        resp_json = requests.post(self.url, headers=self.headers,data=data).json()
        # 提取评论总页数
        if resp_json and resp_json['code'] == 200:
            print(resp_json['data']['comments'])
            count_page = ceil((resp_json['data']['totalCount'] - 15) / 20)
            # page_list=[page for page in range(1,5)]
            # p.map(self.get_comment,page_list)
            # 获取时间戳
            #timeteamp = resp_json['data']['cursor']
        else:
            print("响应数据请求失败")


def main():
    song_id = '1490343020'
    song_name = '如果你也这样过'
    wangyi = WangyiSpider(song_id, song_name)
    wangyi.run()


if __name__ == '__main__':
    main()
