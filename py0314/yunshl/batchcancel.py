import time

import requests

from py0314.NotifyMessage import read_config
from py0314.connectmysql import MysqlClass


def connect_mysql(infos):
    mysql_object = MysqlClass(infos['server_ip'],
                              infos['server_user'],
                              infos['server_pwd'],
                              infos['server_db'])
    return mysql_object


def get_datas(sql_object, infos, sql, text=None):
    ids_data = None
    # 执行sql操作
    sql_result = sql_object.execute_query(infos[sql], text)
    if isinstance(sql_result, list):
        ids_data = [str(sql.pop('sale_order_ids_')) for sql in sql_result]
        print(f"sql查询获取条数:{len(sql_result)}")
    return sql_result, ids_data


def get_header(data_infos):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Content-Type': 'application/json;charset=UTF-8',
        'Proxy-Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        'appsource': 'PC',
        'nonce': 'wG0Zz8vLBncl5nSd2ptC',
        'signnatrue': '1eca8321a9b6d1fc51569db0901f47d9',
        'timestamp': '16805925928783383',
        'yunshl_token': data_infos['yunshl_token']
    }
    return headers


def get_response(data_infos, data, keyword):
    agreement = '' if data_infos['yunshl_domain'].endswith('cn') else 's'  # 正式环境需加上s
    url = data_infos['yunshl_url'].format(agreement,
                                          data_infos['yunshl_id'],
                                          data_infos['yunshl_domain'], keyword)
    headers = get_header(data_infos)
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.json()
    except Exception as e:
        print(e)


def outhouse_invild(data_infos, data_list):
    for item in data_list:
        item['mod_time_'] = item['mod_time_'].strftime('%Y-%m-%d %H:%M:%S')
        invild_data = get_response(data_infos, item, 'invalid')  # 作废出库单
        if invild_data.get('status') and invild_data['data']['form_status_'] == 999:
            print(f"单据：{invild_data['data']['code_']} 作废成功！")
            item['mod_time_'] = invild_data['data']['mod_time_']
            delete_data = get_response(data_infos, item, 'delete')  # 删除出库单
            if delete_data.get('status'):
                print(f"单据：{invild_data['data']['code_']} 删除成功！")
            else:
                print("删除失败！")
        else:
            print("作废失败！")
        time.sleep(1.5)


def main():
    start_flag = input('请确认参数是否已提前设置(输入y or n)：')
    if start_flag.lower() == 'y':
        data_infos = read_config()
        mysql_object = connect_mysql(data_infos['DATABASES_INFO'])
        data_list, ids_data = get_datas(mysql_object, data_infos['DATABASES_INFO'], 'sql_sentence_one')
        if data_list and ids_data:
            print('开始执行批量作废删除出库单操作！')
            outhouse_invild(data_infos['OUTHOUSE_INFO'], data_list)
            print('批量作废删除出库单操作完成！')
            get_datas(mysql_object, data_infos['DATABASES_INFO'], 'sql_sentence_two', text=ids_data)
        else:
            print("没有查询到可以操作的单据")
    else:
        print('请配置好对应的参数再来执行操作吧！')


if __name__ == '__main__':
    main()
