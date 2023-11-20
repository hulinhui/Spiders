import json
import time
from py0314.NotifyMessage import read_config
import requests
from bs4 import BeautifulSoup


class Jd_Follow:

    def __init__(self):
        self.good_follow_list_url = 'https://t.jd.com/follow/product?index={}'
        self.shop_follow_list_url = 'https://t.jd.com/follow/vender?index={}'
        self.seletor_one = 'div.mf-goods-item'
        self.seletor_two = 'div.mf-shop-item'
        self.cancel_good_shop_follow_url = 'https://api.m.jd.com/api'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
            'content-type': 'application/x-www-form-urlencoded',
            'Origin': 'https://t.jd.com',
            'cookie': read_config()['JD']['jd_cookie']
        }

    def get_html(self, url, method='get', params_data=None, data=None):
        try:
            response = requests.request(method=method, url=url, headers=self.headers, params=params_data, data=data)
            response.raise_for_status()
            return response
        except Exception as e:
            print(e)

    def parse_html(self, text, seletor_wd):
        selector = BeautifulSoup(text, 'lxml')
        ids_list = [div.get('id').split('_')[1] for div in selector.select(seletor_wd)]
        return ids_list

    def cancel_good_follow(self, data, page):
        t = str(int(time.time() * 1000))
        skus_str = json.dumps({"skus": ','.join(data)})
        soakey = '2e2i4fRvyfAek5MfHNCe;fMeBpvzbQimFgonJp9YpBqyMcz1VvO4sWcyIBRb8VdOTNQDVo7'
        data_params = {"functionId": "batchCancelFavorite", "body": skus_str,
                       "appid": "follow_for_concert", "soaKey": soakey,
                       "client": "pc", "t": t}
        response = self.get_html(self.cancel_good_shop_follow_url, params_data=data_params)
        if response:
            json_data = response.json()
            print(f"第{page}页商品{json_data.get('resultMsg')}")
        else:
            print(f'第{page}页商品取消关注失败！')

    def cancel_shop_follow(self, data, page):
        t = str(int(time.time() * 1000))
        vends_str = json.dumps({"venderIds": ','.join(data)})
        data_params = {"functionId": "pc_follow_vender_batchUnfollow", "body": vends_str,
                       "appid": "trade_pc_color", "loginType": 3,
                       "client": "pc", "t": t}
        response = self.get_html(self.cancel_good_shop_follow_url, method='post', data=data_params)
        if response:
            print(f'第{page}页店铺取消关注成功！')
        else:
            print(f'第{page}页店铺取消关注失败！')

    def good_follow(self, page):
        while True:
            response = self.get_html(self.good_follow_list_url.format(page))
            if response:
                sku_list = self.parse_html(response.text, self.seletor_one)
                if not sku_list:
                    print('所有商品关注已全部取消')
                    break
                self.cancel_good_follow(sku_list, page)
            else:
                print('获取用户关注商品列表失败！')
            page += 1

    def shop_follow(self, page):
        while True:
            response = self.get_html(self.shop_follow_list_url.format(page))
            if response:
                vender_list = self.parse_html(response.text, self.seletor_two)
                if not vender_list:
                    print('所有店铺关注已全部取消')
                    break
                self.cancel_shop_follow(vender_list, page)
            else:
                print('获取用户关注店铺列表失败！')
            page += 1

    def run(self):
        self.good_follow(1)
        self.shop_follow(1)


if __name__ == '__main__':
    jd_follow = Jd_Follow()
    jd_follow.run()
