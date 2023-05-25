import requests
from fake_useragent import UserAgent


def get_headers():
    token = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI0ODIxNjg3NDYwMzgxNDc3OTM1NDg4OTY3MTYzNTEwNiIsImlhdCI6MTYxMDE2Mjk1OSwiZXhwIjoxNjYwMTQxOTY3LCJyZWZyZXNoX3Rva2VuIjoiNDgyMTY4NzQ2MDM4MTQ3NzkzNTQ4ODk2NzE2MzUxMDYiLCJzY29wZSI6IkFDQ0VTUyIsInN0YXJ0VGltZSI6MTYxMDE2Mjk1OTk4MywiZXhwaXJlc19pbiI6NDk5NzkwMDgsInRva2VuX3R5cGUiOiJQQyIsImxvZ2luIjoiaGxoMjAwIiwiaWQiOjY1Mzg3fQ.T9f1V-dteN8hLSWEzVEm8RRVURPLnsZykbgrYn7REq9t74fYln6VFvEfGvtx-papt91hVJxA6JzR45FeIqac0w'
    headers = {'User-Agent': UserAgent().random, 'yunshl_token': token}
    return headers


def get_data(test_data):
    data = {
        "fileName": "自建商品导入模板v1_0_0.xlsx",
        "colNames": {
            "自建商品基础数据": {
                "a": "商品名称 (必填)",
                "b": "商品编号",
                "c": "商品分类(必填)",
                "d": "基本单位 (必填)",
                "e": "辅助单位1",
                "f": "单位1换算比率",
                "g": "辅助单位2",
                "h": "单位2换算比率",
                "i": "品牌",
                "j": "关联关键词",
                "k": "库存下限",
                "l": "库存上限",
                "m": "商品卖点",
                "n": "是否上架",
                "o": "规格值1 (必填)",
                "p": "规格值2",
                "q": "规格值3",
                "r": "规格名称 (必填)",
                "s": "规格编号",
                "t": "零售价",
                "u": "销售价 (必填)",
                "v": "条形码",
                "w": "分销供货价",
                "x": "商品外部编码"
            },
            "使用说明 - 商品数据录入说明": {
                "a": "自建商品数据录入说明"
            }
        },
        "自建商品基础数据": test_data,
        "使用说明 - 商品数据录入说明": [
            {
                "a": "列名"
            },
            {
                "a": "商品名称"
            },
            {
                "a": "商品编号"
            },
            {
                "a": "商品分类"
            },
            {
                "a": "基本单位"
            },
            {
                "a": "辅助单位1"
            },
            {
                "a": "单位1换算比率"
            },
            {
                "a": "辅助单位2"
            },
            {
                "a": "单位2换算比率"
            },
            {
                "a": "品牌"
            },
            {
                "a": "关联关键词"
            },
            {
                "a": "库存下限"
            },
            {
                "a": "库存上限"
            },
            {
                "a": "商品卖点"
            },
            {
                "a": "是否上架"
            },
            {
                "a": "规格值1"
            },
            {
                "a": "规格值2"
            },
            {
                "a": "规格值3"
            },
            {
                "a": "规格名称"
            },
            {
                "a": "规格编号"
            },
            {
                "a": "零售价"
            },
            {
                "a": "销售价"
            },
            {
                "a": "条形码"
            },
            {
                "a": "分销供货价"
            },
            {
                "a": "商品外部编码"
            }
        ]
    }
    return data


def get_test_data():
    data_list = []
    for i in range(1, 3):
        data_format = {
            "a": "导入商品测试1",
            "b": f"QP0005{i}",
            "c": "饮料3",
            "d": "PCS",
            "e": "D",
            "f": "2",
            "g": "K",
            "h": "6",
            "o": "规格K22",
            "i": "品牌测试",
            "j": "1,2,3,4",
            "k": "0",
            "l": "12",
            "m": "商品卖点",
            "n": "是",
            "p": "规格K",
            "q": "333",
            "r": "规格/颜色/pd",
            "s": f"202011240009{i}",
            "u": "95.66",
            "t": "150",
            "v": f"txm888{i}",
            "w": "100",
            "x": "wb999001"
        }
        data_list.append(data_format)

    return data_list


def get_result(data, headers):
    import_url = 'http://store2081.ysdh6.cn/v1/goods/goodsDraft/batchImport?nonce=yunshl20200101'
    r = requests.post(import_url, json=data, headers=headers)
    if r.status_code == 200:
        json_data = r.json()
        if json_data['status'] == 1 and json_data['data']['success_count_'] != 0:
            print('导入成功')
        elif json_data['status'] == 0:
            print(json_data['message'])
        else:
            fail_info = json_data['data']['failExcel']['sheets']['自建商品基础数据'][1]['aa']
            print(f'导入失败,失败原因:{fail_info}')
    else:
        print('接口状态非200')
        print(r.json())


def main():
    headers = get_headers()
    test_data = get_test_data()
    data = get_data(test_data)
    get_result(data, headers)


if __name__ == '__main__':
    main()
