import pymssql
from py0314.NotifyMessage import read_config


class HandleSqlServer:
    def __init__(self, ms_ip, ms_user, ms_pwd, ms_db, ms_charset):
        self.host = ms_ip
        self.user = ms_user
        self.pwd = ms_pwd
        self.db = ms_db
        self.charset = ms_charset
        self.conn = self.__ms_get_conn()
        self.cursor = self.__ms_get_cursor()

    def __ms_get_conn(self):
        print("[MSSQL]开始进行数据库连接！")
        try:
            conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd,
                                   database=self.db, charset=self.charset, as_dict=True)
            return conn
        except Exception as e:
            print(f'[MSSQL]数据库:{self.db} 连接失败!')
            exit()

    def __ms_get_cursor(self):
        if not self.conn:
            return None
        return self.conn.cursor()

    def execute_query(self, sql_content, text=None):
        try:
            if isinstance(text, list):
                self.cursor.executemany(sql_content, text)  # 执行多条操作
            else:
                self.cursor.execute(sql_content, text)  # 执行单条操作
            if sql_content.split()[0].lower() == 'select':
                print('[MSSQL]开始执行查询语句sql！')
                return self.cursor.fetchall()
            else:
                print("[MSSQL]开始执行非查询语句sql！")
                self.conn.commit()
                print(f"[MSSQL]√执行成功，影响行数:{self.cursor.rowcount}")
                return self.cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            print(e)

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print('[MSSQL]全部执行完毕，关闭数据库连接！')


def main():
    ms_infos = read_config()['MS_SQL_INFO']
    ms_object = HandleSqlServer(**ms_infos)
    sql_content = 'SELECT TOP(1000) [ID] ,[FID] ,[FEntryID] ,[TemplateType] ,[BillNo] ,[OrderCode] ,[SupplierName] ,[StockName] ,[Sku] ,[BigCode] FROM [QATest].[dbo].[QA_TestInspection_Template]'
    item_data = ms_object.execute_query(sql_content)
    for item in item_data:
        print(item)


if __name__ == '__main__':
    main()
