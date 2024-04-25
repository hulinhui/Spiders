import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from py0314.FormatHeaders import get_format_headers, header_rl
from py0314.logger_tools import Handle_Logger
import copy


def get_data():
    multipart_encoder = MultipartEncoder(fields={
        'BillNo': 'test202404250003',
        'OrderCode': 'DH202404250003',
        'SupplierName': '深圳市湘凡科技有限公司',
        'Sku': '15079',
        'StockName': 'B2B共享仓',
        'Qty': '10',
        'QAtype': '回仓验货',
        'PlanName': '免检',
        'Checkamount': '150',
        'Testamount': '120',
        'Checkeffect': '20',
        'Testeffect': '10',
        'Selfeffect': '10',
        'CheckResult': '不合格',
        'InAmount': '10',
        'ReceiveAmount': '0',
        'Checkunpass': '0',
        'Testunpass': '0',
        'PackageRejectsQty': '2',
        'Unpassperty': '包装不良',
        'UnpassKind': '条码不良',
        'UnRemark': '条码模糊、条码漏贴、条码贴歪贴错位置、条码错误、跳格、无法扫描、条码混用',
        'RiskRank': 'B',
        'Damages': '100',
        'CheckPerson': 'hulinhui',
        'TestPerson': 'hlh',
        'SQE': '聂星星',
        'SQECode': ',0005',
        'Purchase': '李庆珍',
        'PurchaseCode': ',0007',
        'Describe': '我是问题描述信息',
        'Attachment': '',
        'Remark': '我是备注信息'
    }, boundary='----WebKitFormBoundarygSZMxzZMA6onZWwv')
    return multipart_encoder


class InspectionList:
    def __init__(self, post_data):
        self.add_edit_url = 'http://192.168.1.204:27621/Testtype/AddInspection'
        self.query_url = 'http://192.168.1.204:27621/Testtype/GetInspectionGrid'
        self.delete_url = 'http://192.168.1.204:27621/Testtype/InspectionDelete'
        self.headers = get_format_headers(header_rl)
        self.log = Handle_Logger.HandleLog()
        self.post_data = post_data

    def get_response(self, url, headers, method='POST', data=None):
        try:
            response = requests.request(method=method, url=url, headers=headers, data=data)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response
        except Exception as e:
            self.log.error(e)

    @staticmethod
    def check_result(response, return_flag=None):
        json_data = response.json() if response else {}
        result = json_data['staus'] if json_data and 'staus' in json_data else ''
        is_success = True if result == 'success' else False
        if return_flag:
            return is_success
        else:
            return json_data

    def add_inspection(self):
        headers = copy.deepcopy(self.headers)
        headers['Content-Type'] = 'multipart/form-data; boundary=----WebKitFormBoundarygSZMxzZMA6onZWwv'
        add_response = self.get_response(url=self.add_edit_url, headers=headers, data=self.post_data)
        success_flag = self.check_result(add_response)
        if success_flag:
            self.log.info('新增成功!')
        else:
            self.log.info('新增失败!')

    def query_inspection(self):
        query_data = {"page": "1", "rows": "50"}
        query_response = self.get_response(self.query_url, self.headers, data=query_data)
        result_data = self.check_result(query_response)
        query_list = [str(row.get('FID')) for row in result_data['rows'] if
                      row['CheckPerson'] == 'hulinhui'] if 'rows' in result_data else []
        query_ids = ','.join(query_list)
        return query_ids

    def delete_inspection(self, ids):
        delete_data = {'IDS': ids}
        delete_response = self.get_response(url=self.delete_url, headers=self.headers, data=delete_data)
        success_flag = self.check_result(delete_response, return_flag=True)
        if success_flag:
            self.log.info('删除成功!')
        else:
            self.log.info('删除失败!')

    def run(self):
        self.add_inspection()
        query_ids = self.query_inspection()
        self.log.info(f'查询当前垃圾数据fid为，{query_ids}')
        if query_ids:
            self.delete_inspection(query_ids)
        else:
            self.log.info('暂无垃圾数据，不需要删除！')


def main():
    post_data = get_data()
    il = InspectionList(post_data)
    il.run()


if __name__ == '__main__':
    main()
