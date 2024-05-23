import json
import time
from urllib.parse import quote

import requests
from lxml import etree
from py0314.NotifyMessage import read_config


class JdEvaluate:
    """docstring for Jd_Evaluate"""

    def __init__(self):
        super(JdEvaluate, self).__init__()
        self.comment_url = 'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc' \
                           '&clientVersion=1.0.0&t={}&loginType=3&body={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
            'Accept': 'application/json,text/javascript,*/*;q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded'}
        self.wait_comment_url = 'https://club.jd.com/myJdcomments/myJdcomment.action?sort=0'
        self.service_comments_url = 'https://club.jd.com/myJdcomments/insertRestSurvey.action?voteid=145&ruleid={}'
        self.save_product_coment_url = 'https://club.jd.com/myJdcomments/saveProductComment.action'
        self.orderVoucher_url = 'https://club.jd.com/myJdcomments/orderVoucher.action?ruleid={}'
        self.headers[
            'cookie'] = read_config()['JD']['jd_cookie']

    def get_data(self, url, method='GET', headers=None, data=None):
        if method.lower() == 'get':
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                return response
            except Exception as e:
                print(e)
                return None
        else:
            try:
                response = requests.post(url, headers=headers, data=data)
                response.raise_for_status()
                response.encoding = 'gbk'
                return response
            except Exception as e:
                print(e)
                return None

    def order_comments_sku(self, order_id):
        sku_list = []
        response = self.get_data(self.orderVoucher_url.format(order_id))
        if response:
            select_word = etree.HTML(response.text)
            div_list = select_word.xpath('//div[@class="form-part1"]//div[@class="comment-goods"]')
            for div in div_list:
                sku_id = div.xpath('./div[@class="p-name"]/a/@href')[0].split('/')[-1].split('.')[0]
                sku_list.append(sku_id)
        else:
            print('获取订单评价接口错误')

        return sku_list

    @staticmethod
    def processing_data(data):
        if data:
            result_dict = json.loads(data.text)
            if 'comments' in result_dict and result_dict.get('comments'):
                return result_dict['comments']
            else:
                return None
        else:
            print('获取商品评价接口错误！')

    @staticmethod
    def get_comment_pic(comment_data):
        if 'images' in comment_data:
            return [f"{img_dic['imgUrl']}" for img_dic in comment_data.get('images')]
        else:
            return []

    @staticmethod
    def get_encode_body(product_id):
        body_dcit = {"productId": product_id, "score": 0, "sortType": 5, "page": 0, "pageSize": 10, "isShadowSku": 0,
                     "fold": 1,
                     "bbtf": "", "shield": ""}
        body_text = quote(json.dumps(body_dcit).replace(' ', ''))
        return body_text

    def collection_comment(self, product_id):
        comment_list = []
        tamp_times = int(round(time.time() * 1000))
        body_text = self.get_encode_body(product_id)
        response = self.get_data(self.comment_url.format(tamp_times, body_text))
        comment_data = self.processing_data(response)
        if comment_data:
            for data in comment_data:
                comments = data['content']
                images = self.get_comment_pic(data)
                comment_list.append((comments, images))
        return comment_list

    def service_coments(self, order_id):
        data = {'oid': order_id, 'gid': '69', 'sid': '549656', 'stid': '0', 'tags': '', 'ro1827': '1827A1',
                'ro1828': '1828A1', 'ro1829': '1829A1'}
        result_data = self.get_data(self.service_comments_url.format(order_id), method='POST', headers=self.headers,
                                    data=data)
        if result_data:
            json_data = result_data.json()
            if 'status' in json_data and json_data.get('status') == 1:
                print(f'订单:{order_id},服务评价成功!')
            elif 'status' in json_data and json_data.get('status') == -3:
                print(f'订单:{order_id},已经服务评价过了!')
            else:
                print(f'订单:{order_id},服务评价失败')
        else:
            print('服务评价接口请求失败')

    def get_random_comment(self, sku_id):
        comment_list = self.collection_comment(sku_id)
        if comment_list:
            sort_list = sorted(comment_list, key=lambda x: len(x[1]), reverse=True)
            content_text = quote(quote(sort_list[0][0].encode('utf-8'), 'utf-8'), 'utf-8')
            # print(content_text)
            content_img = quote(
                ','.join(['//img30.360buyimg.com/shaidan/' + url.split('_')[1] for url in sort_list[0][1]]), 'utf-8') if \
                sort_list[0][1] else None
            # print(content_img)
            return content_text, content_img
        else:
            return None, None

    def executive_comment(self, order_id, sku_id):
        content_text, content_img = self.get_random_comment(sku_id)
        if content_text:
            if content_img:
                data = f'orderId={order_id}&productId={sku_id}&score=5&content={content_text}&imgs={content_img}&saveStatus=2&anonymousFlag=1'
            else:
                data = f'orderId={order_id}&productId={sku_id}&score=5&content={content_text}&saveStatus=1&anonymousFlag=1'
            headers = {'X-Requested-With': 'XMLHttpRequest'}
            headers.update(self.headers)
            result_data = self.get_data(self.save_product_coment_url, method="post", headers=headers, data=data)
            if result_data:
                json_data = result_data.json()
                if 'success' in json_data and json_data.get('success'):
                    print(f"订单:{order_id},商品{sku_id}评价成功！")
                else:
                    print(f"订单:{order_id},商品{sku_id}评价失败！[失败原因:{json_data['error']}]")
            else:
                print(f"订单:{order_id},商品{sku_id}评价失败[Interface error]！")
        else:
            print(f"订单:{order_id},商品{sku_id}评价失败！[商品无评价]")

    def run(self):
        html = self.get_data(self.wait_comment_url)
        selector_word = etree.HTML(html.text)
        tbody_tag = selector_word.xpath('//div[@class="mycomment-table"]//tbody')
        if tbody_tag:
            print(f'一共获取了{len(tbody_tag)}个需要评价的记录！')
            for tbody in tbody_tag:
                order_id = tbody.xpath('./tr[@class="tr-th"]//span[@class="number"]/a/text()')[0].strip()
                self.service_coments(order_id)  # 服务评价
                sku_ids = self.order_comments_sku(order_id)  # 获取评价订单页面sku[有些商品评价页获取sku与实际评论的sku不一致]
                if sku_ids:
                    print(f'订单:{order_id},总共有{len(sku_ids)}个商品需要评价!')
                    for sku_id in sku_ids:
                        self.executive_comment(order_id, sku_id)  # 商品评价
                        print('###################################')
                        time.sleep(3)  # 防止提交过快，导致提交失败
                else:
                    print(f'订单:{order_id},无商品需要评价...')

            print('全部订单评价完成！！！')
        else:
            print('无需要待评价的订单')


if __name__ == '__main__':
    jd_ev = JdEvaluate()
    jd_ev.run()
