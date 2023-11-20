import json
import re
from urllib.parse import quote
import time
import requests
from lxml import etree


class Jd_Evaluate:
    """docstring for Jd_Evaluate"""

    def __init__(self):
        super(Jd_Evaluate, self).__init__()
        self.comment_url = 'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_skuProductPageComments&client=pc' \
                           '&clientVersion=1.0.0&t={}&loginType=3&productId={' \
                           '}&score=0&sortType=5&page=0&pageSize=15&isShadowSku=0&fold=1 '
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
            'cookie'] = 'shshshfpa=563fd11c-0c38-6029-96c8-8f579f93ced5-1678164306; shshshfpx=563fd11c-0c38-6029-96c8-8f579f93ced5-1678164306; shshshfp=e6f68a8e2fa6bd2edee7ba62dfb045cd; user-key=4d0bdcd1-51af-455c-a03b-6ae064006d24; cn=5; unpl=JF8EAKdnNSttWxhTAEgFGBYYGA8BWwkLT0QHbmFVBloLHFwFT1VMQRh7XlVdXxRLFx9vYRRUXFNJVQ4YBCsVEUtcVVZtC0oVAmlgA1JYXntkNRgCKxMgS1pcVlgATBMKa2YHU1RaTF0NEwQcFSBKbVRWWjh7JwZvZgVVWllLVgMrAysQEEpcVl9ZDE8WMyQJBBldX0NcABMFHxsUSl9TV18PQh8LaWACZFxoSA; areaId=19; PCSYCityID=CN_440000_440300_0; __jdv=76161171|ntp.msn.cn|t_2030767747_|jingfen|2b64b6259bcd4e25b507ac6bf91effb9|1700188263288; jsavif=0; ipLoc-djd=19-1607-4773-62121; TrackID=1EHGBAZDVCiYoCP_B3pUAJByrr_fh1tik-PGzahBjS3t716cFsSsIx5IbubQZn9cz_1Rxx02HAr3Pv70qQz6L4ATFmDqYCnDgcfw37hcoQnLWY1w3mT1pIXnw4a_SnchH; thor=B70169661C900064F0D2E26658EC144B6BACF59C113B01D8BB40AAE0DBEB2D09C8D0DEB713B7C8A7DE407DFA6A98FC08BBFCD4F6AD93B732617A5C27F083CA690492297A94CF419A51699B6873DAB3206E43A1A86C20E2AC3FB8A0022F2B2C0BCCC724C634F2DE46DB7E65A3D57B0EE2E0ACABB27549CF879CB5C9E3BBF230920DAFC040C60086EBF36CE29148144E570A04460C0B9BA6AD007EAE6C40A3DA56; flash=2_SkZElLVBZAzonC3IXnwDhoqg3-KEcj1Cfc5ILWvjb65DaxdYfpfhBHkVKIvLoHwVVzLVvxf55C6fO4Tc09AF8fd5Bo4QXGYBeA2nm5tkd-p*; pinId=61F1TNdwLhBszIHFJtsEpw; pin=jd_rRhnMUyjukur; unick=jd_rRhnMUyjukur; ceshi3.com=201; _tp=EQxZRWvG%2Fz7U5rgK5u1Kbg%3D%3D; _pst=jd_rRhnMUyjukur; shshshsID=7aa0106d9e7b4bc4920e57a6c8386a1a_4_1700188450750; shshshfpb=AAqntINuLEj_RHAw4YCmWyI9Xn5PO1RZ4FkMGRAAAAAA; __jda=122270672.1699496585036836899766.1699496585.1699496585.1700188229.2; __jdc=122270672; __jdb=122270672.16.1699496585036836899766|2.1700188229; 3AB9D23F7A4B3C9B=XCE7GAZVX2WKZCD5S6S6LNW6PQWZR2BVMBM2VBP74ELXGF5UTC337Z5XR3AG2LOJMPYQORVOMI7OJSXSBFFNUNAGDI'

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

    def collection_comment(self, product_id):
        comment_list = []
        tamp_times = int(round(time.time() * 1000))
        response = self.get_data(self.comment_url.format(tamp_times, product_id))
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
    jd_ev = Jd_Evaluate()
    jd_ev.run()
