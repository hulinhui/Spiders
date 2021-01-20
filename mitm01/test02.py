import json
import os


path='./'

def response(flow):
    url='http://api.yimaideng.cn/v1/shop/order/searchListForShop?'
    if flow.request.url.startswith(url) and flow.response.status_code==200 and flow.request.method.lower()=='get':
        text=flow.response.text
        json_data=json.loads(text)
        if json_data['status']==1 and 'data'in json_data:
            order_list=json_data['data']['pdList']
            if order_list:
                for order in order_list:
                    item={}
                    item['client_name_']=  order['client_name_']
                    item['code_'] = order['code_']
                    item['order_total_'] = order['order_total_']
                    item['create_time_'] = order['create_time_']
                    item['finance_status_'] = order['finance_status_']
                    item['goods_count_'] = order['goods_count_']
                    item['ship_way_'] = order['ship_way_']
                    item['company_id_'] = order['company_id_']
                    #保存数据
                    save(item)
            else:
                print('暂无单据')



def save(item):
    if not os.path.exists(path):
        os.mkdir(path)
    with open(f'{path}订单数据.json','a',encoding='utf8') as f:
        f.write(json.dumps(item)+'\n')



