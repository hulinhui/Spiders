# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         select_excel
# Description:  
# Author:       hulinhui779
# Date:      2024/3/4 14:16
# -------------------------------------------------------------------------------
from py0314.read_excel import ReadExcelChenShi
from py0314.connectmysql import MysqlClass
from py0314.NotifyMessage import read_config


def dict_cover_tuple(dict_data, key):
    return tuple([str(item[key]) for item in dict_data])


def get_sql_and_excel_object(data_info):
    myexcel_object = ReadExcelChenShi(data_info['cs_file_path'])
    mysql_object = MysqlClass(data_info['cs_server_ip'], data_info['cs_server_user'],
                              data_info['cs_server_pwd'],
                              data_info['cs_server_db'])
    return mysql_object, myexcel_object


def select_data(sql_object, tuple_data, sql_text):
    sql_result = sql_object.execute_query(sql_text, tuple_data)
    return sql_result


def main():
    # 1、连接数据库及从excel读取数据
    databases_info = read_config()['CS_DATABASES_INFO']
    mysql_object, excel_object = get_sql_and_excel_object(databases_info)
    excel_data = excel_object.read_data()
    ordercodes = excel_object.excel_order_count()
    print(f'当前excel涉及{len(set(ordercodes))}个订单数据,总共{len(ordercodes)}条记录')

    # 第一次查询数据：查询满足条件的订单id
    ordercode_tup = dict_cover_tuple(excel_data, '订货单号')
    first_sql_result = select_data(mysql_object, (ordercode_tup,), databases_info['cs_sql_sentence_one'])
    print(f'第1次过滤记录数据：符合条件单据条数---{len(first_sql_result)}条')

    # 第二次查询数据：根据订单id及规格编号查询满足条件的订货清单条数
    orderid_tup = dict_cover_tuple(first_sql_result, 'id_')
    productcode_tup = dict_cover_tuple(excel_data, '规格编号')
    sql_two_result = select_data(mysql_object, (orderid_tup, productcode_tup), databases_info['cs_sql_sentence_two'])
    print(f'第2次过滤记录数据：符合清单条数---{len(sql_two_result)}条')

    # 判断数量是否满足条件
    # out_number_tup = dict_cover_tuple(excel_data, '出库数量')
    # print(out_number_tup)


if __name__ == '__main__':
    main()
