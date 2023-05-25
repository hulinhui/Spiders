# -*- coding: utf-8 -*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         order_test
# Description:  
# Author:       hlh
# Date:      2021/1/1 23:02
#-------------------------------------------------------------------------------
import hmac
import json

import requests
import hashlib
from fake_useragent import UserAgent
import time
import base64,urllib.parse
import logging
from apscheduler.schedulers.blocking import BlockingScheduler


logging.basicConfig(level=logging.INFO,filename='bugorder.log',filemode='a',format='%(asctime)s-%(lineno)d-%(levelname)s:%(message)s')
client_account='xd0001'
client_password='123456'


class YsDing():
    def __init__(self,account,password):
        self.account=account
        self.password=self.md5_password(password)
        self.good_name='下单商品测试'
        self.number=2
        self.headers={"User-Agent":UserAgent().random,"yunshltoken":'null'}
        self.login_url='https://api.ysdinghuo.com/v1/account/mixedLogin?'
        self.good_url='https://api.ysdinghuo.com/v1/shop/goods/noAuth/searchListForShop?webApp_=1&company_=1879&keyword_={}'
        self.save_url='https://api.ysdinghuo.com/v1/shop/order/save'
        self.pay_url='https://api.ysdinghuo.com/v1/shop/order/combinationPay'
        self.text=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'下单情况：\n'

    def dingding_api(self,message):
        timestamp = str(round(time.time() * 1000))
        secret = 'SEC2d77d36b7113ba8070d1a3d2049c739ba841f9bf147c58c5f5522749e02c8a26'
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        web_hook_url = 'https://oapi.dingtalk.com/robot/send?access_token=c11d49c3264e22f50814e3477c4ed38c157a15a8d5cf594cbff5a65785e70fce'
        dingding_url = web_hook_url + f'&timestamp={timestamp}&sign={sign}'
        self.send_message(dingding_url, message)

    def send_message(self,url, text):
        json_text = {"msgtype": "text", "text": {"content": text}}
        headers = {'Content-Type': 'application/json'}
        resp = requests.post(url, data=json.dumps(json_text), headers=headers).json()
        code = resp["errcode"]
        currenttime = time.strftime("%Y-%m-%d %X")
        if code == 0:
            # print(currenttime + ":消息发送成功 返回码:" + str(code) + "\n")
            logging.warning("消息发送成功 返回码:{}\n".format(code))
        else:
            # print(currenttime + "消息发送失败 返回码:" + str(code) + "\n")
            logging.warning("消息发送失败 返回码:{}\n".format(code))


    def md5_password(self,password):
        m=hashlib.md5()
        m.update(password.encode('utf-8'))
        return m.hexdigest()

    def get_requests(self,url,method='get',data=None,flag=True):
        if method.lower()=='post' and flag:
            response=requests.post(url,data=data,headers=self.headers)
            if response.status_code==200:
                return response
        elif  method.lower()=='post' and not flag:
            response = requests.post(url, json=data, headers=self.headers)
            if response.status_code == 200:
                return response
        else:
            response = requests.get(url,headers=self.headers)
            if response.status_code==200:
                return response

    def login(self):
        data={"phone_":self.account,"password_":self.password}
        response=self.get_requests(self.login_url,'post',data=data)
        if response:
            json_data=response.json()
            if json_data['status']==1 and json_data['message']=='操作成功':
                client_name=json_data['data']['loginUser']['client_name_']
                token_=json_data['data']['loginUser']['token_']
                self.headers.update({"yunshltoken": token_})
                self.text+=f'{client_name}:登录成功!'
                # print(f'{client_name}:登录成功!')
            else:
                self.text+=f"登录失败:{json_data['message']}"
                # print(f"登录失败:{json_data['message']}")
        else:
            self.text+=f'访问失败-状态码：{response.status_code}'
            # print('接口访问失败')

    def search_good(self):
        response=self.get_requests(self.good_url.format(self.good_name))
        if response:
            json_data=response.json()
            good_data=json_data['data']['pdList']
            if json_data['status']==1 and len(good_data):
                good_info = {}
                good_data=good_data[0]['productList'][0] #取第一个商品第一个规格数据
                good_info['cart_number_']=self.number
                good_info['cubage_'] = good_data['cubage_']
                good_info['goods_id_'] = good_data['goods_id_']
                good_info['id_'] = good_data['id_']
                good_info['unit_id_'] = good_data['unit_id_']
                good_info['unit_name_'] = good_data['unit_name_']
                good_info['weight_'] = good_data['weight_']
                return good_info
            else:
                print('查询商品数据失败')
        else:
            print('查询商品接口状态有误')

    def post_data(self,item):
        data={
            "_meth":"body",
            "company_id_":"1879",
            "ship_way_":"3",
            "link_name_":"lxr",
            "link_phone_":"13255567777",
            "link_region_":"广东 茂名 高州市",
            "link_region_ids_":"5,84,776",
            "link_address_":"我是详细信息",
            "invoice_":0,
            "invoice_head_":"胡",
            "invoice_content_":"商品类别",
            "invoice_code_":"0213235",
            "expect_time_":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
            "remark_":"测试自动下单数据",
            "attachment_":"[]",
            "from_":3,
            "productList":[item],
            "additional_fee_json_":" ",
            "freeGoodsList":[]
        }
        return data


    def save_order(self,item):
        data=self.post_data(item)
        response=self.get_requests(self.save_url,'post',data=data,flag=False)
        if response:
            json_data=response.json()
            if json_data['status']==1:
                data=json_data['data']
                self.text+='\n{}下单成功!!,单号为：{}'.format(data['client_name_'],data['code_'])
                # print('{}下单成功!!,单号为：{}'.format(data['client_name_'],data['code_']))
                return data['id_'],data['mod_time_'],data['order_total_'],data['code_']
            else:
                self.text+=f'\n下单失败2:{json_data["message"]}'
                # print(f'下单失败2:{json_data["message"]}')
        else:
            self.text+=f'\n下单失败1-状态码：{response.status_code}'
            # print(f'下单失败1-状态码：{response.status_code}')


    def pay_data(self,tuple,pay_type):
        data={
            "_meth":"body",
            "sale_order_id_":tuple[0],
            "sale_order_mod_time_":tuple[1],
            "pre_balance_param_":{"pay_type_":pay_type,"pay_money_":tuple[2],"order_id_":tuple[0],"order_mod_time_":tuple[1]}
            }
        return data


    def pay_order(self,order_info,pay_type=4):
        if order_info:
            pay_data=self.pay_data(order_info,pay_type)
            response=self.get_requests(self.pay_url,'post',data=pay_data,flag=False)
            if response:
                json_data=response.json()
                if json_data['status']==1:
                    pay_money=json_data['data']['income_']
                    if pay_money==order_info[2]:
                        # print(f'订单号：{order_info[3]},支付金额：￥{pay_money},支付成功！！')
                        self.text+=f'\n订单号：{order_info[3]},支付金额：￥{pay_money},支付成功！！'
                    else:
                        self.text+=f'\n支付失败'
                else:
                    self.text+=f"\n支付失败,失败原因:{json_data['message']}"
                    # print(f"支付失败,失败原因:{json_data['message']}")
        else:
            self.text+=f"\n支付失败，订单信息获取失败"
            # print('支付失败，订单信息获取失败')

    def buy_order(self):
        #查询商品
        good_dict=self.search_good()
        #下单
        if good_dict:
            order_info=self.save_order(good_dict)
            self.pay_order(order_info)
        else:
            # print('获取商品信息失败')
            self.text+='\n获取商品信息失败'
    def send_info(self):
        self.dingding_api(self.text)
        print('消息发送成功')

def main():
    yunshl = YsDing(client_account, client_password)
    yunshl.login()
    yunshl.buy_order()
    yunshl.send_info()

if __name__=='__main__':
    scheduler=BlockingScheduler()
    scheduler.add_job(main,'cron',hour=20,minute=21)
    scheduler.start()