import requests
from bs4 import BeautifulSoup
import time
import json


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
            'cookie': '__jdu=1678164304783978463064; shshshfpa=563fd11c-0c38-6029-96c8-8f579f93ced5-1678164306; shshshfpx=563fd11c-0c38-6029-96c8-8f579f93ced5-1678164306; shshshfpb=l1v9Yu5XYm5e3-You_geg3A; areaId=19; PCSYCityID=CN_440000_440300_0; user-key=76f491b9-05ef-4f5f-a5c7-890c844e9b53; ipLoc-djd=19-1607-4773-62121; mt_xid=V2_52007VwMVVFRYVV8dSBxaDGULFFtYX1BbGEwpVAxkUxAAWwpOD08eGUAAYQNCTlUPVlwDQEtUAjMDEgZYX1BTL0oYXwd7AhdOXVFDWhlCGl4OZAMiUm1YYloeThFUAWELFlFeaFZeHEs%3D; shshshfp=b0a6839ffce9e007b681c91742e05cd9; unpl=JF8EAMlnNSttCx9cBRkHEhsXHg8HW15cTEQCbzdRVV9bTlBSSAFJE0B7XlVdXxRKEh9sZxRUWVNJUQ4aBysSEXtdVV9cCUIfCmdlNVRZXyVVaxsLHnx-TFxcDFhYSR8AbGYHBw1fHmQ1GAIrEyBLWlJXXQ9OFQJqYQxWVV5CUQIZAxwXIEptVFZZOEsWAmllA1VUWUtXAhMKKyIUTV5SWlwJShQzblcEZBw2S1cDHAcTERYGXVNYVAhMEgFuYgNdX1BNXQAcABoVFXtcZF0; __jdv=122270672|www.linkstars.com|t_1000089893_156_0_184__609c4a392203ba6d|tuiguang|be9134886dcb42e6b01ae03245fb2c0a|1682062446720; TrackID=1c8_PamEIWjzm-lRR2TgCFSnR7vtPOzWLN5gpBSyiB7ID5kxugh7L9dzE_6Xmcj1t9w0DbZvhndDOHu7whC4yn1aN6kpYzF1vp5adnF-9WGWQ2GVGyUn-Z1An-wc2Qr0U; pinId=61F1TNdwLhBszIHFJtsEpw; pin=jd_rRhnMUyjukur; unick=jd_rRhnMUyjukur; ceshi3.com=201; _tp=EQxZRWvG%2Fz7U5rgK5u1Kbg%3D%3D; _pst=jd_rRhnMUyjukur; shshshsID=515ee3ad0a27912e2349b53878f56dbd_2_1682064602267; __jda=122270672.1678164304783978463064.1678164304.1682062447.1682064567.17; __jdc=122270672; p-request-id=jd_rRhnMUyjukur2023042116ZYC9asHppC; thor=B70169661C900064F0D2E26658EC144B6BACF59C113B01D8BB40AAE0DBEB2D09F816AEBAAF845DC4DC3C8D081E103FA3556AD1665929FB81075E2C995CEE33470D5114E1A94069224130A34CA8B958A8608EDC576F19D50974D15DB620D607B09733333852BFC05B2F9DBE11EF5429D480BA03E2FC55E7C7A19D3F6D6CAA1B04763A8127DF222ABC0851FBB7E08E2B103C6042DA55884A8A6A2361A06C1B5AC4; cn=3; __jdb=122270672.12.1678164304783978463064|17.1682064567; 3AB9D23F7A4B3C9B=XCE7GAZVX2WKZCD5S6S6LNW6PQWZR2BVMBM2VBP74ELXGF5UTC337Z5XR3AG2LOJMPYQORVOMI7OJSXSBFFNUNAGDI'
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
