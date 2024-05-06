import re

import openpyxl
import os


class ProbationExcel:
    def __init__(self, path, name=None):
        self.file_path = path
        self.workbook, self.sheet = self.__open_excel(name)

    def __str__(self):
        return f'当前excel信息:总共{self.__excel_max_row()}行{self.__excel_max_cols()}列'

    def __open_excel(self, name):
        if not os.access(self.file_path, os.F_OK):
            raise FileNotFoundError('Excel文件不存在！')
        if not os.access(self.file_path, os.R_OK):
            raise IOError('Excel文件读写错误！')
        workbook = openpyxl.load_workbook(self.file_path)
        if name:
            sheet = workbook[name]
        else:
            sheet = workbook.active  # 获取默认sheet
        return workbook, sheet

    def __excel_max_row(self):
        return self.sheet.max_row

    def __excel_max_cols(self):
        return self.sheet.max_column

    def get_row_data(self, min_row, max_col):
        return list(next(self.sheet.iter_rows(min_row=min_row, max_col=max_col, values_only=True)))

    def user_info_tips(self):
        userinfo_list = [re.sub(r'\s+', '', data) for data in self.get_row_data(3, 9) if data]
        name_text, department_name, *c, employment_date = userinfo_list
        department_name = '部门：' + department_name
        name_text = name_text.strip('部门：')
        print(name_text, department_name, *c, employment_date)

    def write_sheet(self, row, col, value):
        if value:
            self.sheet.cell(row, col).value = value

    @staticmethod
    def read_data(row_data):
        if row_data[1]:
            print(f'{row_data[1]}工作计划如下:')
        print(f'工作内容：{row_data[2]};\n时间段：{row_data[4]}~{row_data[5]};')
        print('-' * 50)

    def write_data(self, rows, cols, is_remark=None):
        try:
            remark = None
            value = int(input('当前任务是否完成？1、是 2、否:'))
            if is_remark:
                remark = input('请输入备注信息！')
            if value == 1:
                self.write_sheet(rows, cols, '是')
                self.write_sheet(rows, cols + 2, remark)
            elif value == 2:
                reason = input('你未完成任务，需要填写未完成的原因：')
                self.write_sheet(rows, cols, '否')
                self.write_sheet(rows, cols + 1, reason)
                self.write_sheet(rows, cols + 2, remark)
            else:
                print('输入有误,跳过不保存')
        except Exception:
            print('非法字符，跳过不保存')

    def run(self, min_row, max_col, is_write=False):
        is_have_plan = True
        for index, row_value in enumerate(self.sheet.iter_rows(min_row=min_row,
                                                               max_col=max_col,
                                                               values_only=True), 0):
            index += min_row
            if not any(row_value[2:6]) or row_value[6]:
                continue
            self.read_data(row_value)
            if is_write:
                self.write_data(index, cols=7)
            is_have_plan = False
        if is_write:
            self.workbook.save(self.file_path)
        if is_have_plan:
            print('太棒了，你的任务都完成了!')
        self.__close()

    def __close(self):
        self.workbook.close()


if __name__ == '__main__':
    file_path = r'\\Filesvr\综合支持中心\信息管理部\周工作任务\07 测试组\06 胡林辉\胡林辉-试用期工作计划表.xlsx'
    excel = ProbationExcel(file_path)
    excel.user_info_tips()
    excel.run(5, 9)
