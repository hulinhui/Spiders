import pymysql
from py0314 import NotifyMessage


class MysqlClass:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.conn = self.__get_conn()
        self.cursor = self.__get_cursor()

    # 创建连接
    def __get_conn(self):
        print("[SQL]开始进行数据库连接！")
        try:
            conn = pymysql.connect(host=self.host, port=3306, user=self.user, password=self.pwd,
                                   database=self.db)
            return conn
        except Exception as e:
            print(f'[SQL]数据库:{self.db} 连接失败!')
            exit()

    # 获取游标
    def __get_cursor(self):
        if self.conn is not None:
            return self.conn.cursor(pymysql.cursors.DictCursor)

    # 执行sql
    def execute_query(self, sql_content, text=None):
        try:
            if text:
                self.cursor.executemany(sql_content, text)  # 执行多条操作
            else:
                self.cursor.execute(sql_content)  # 执行单条操作
            if sql_content.split()[0].lower() == 'select':
                print('[SQL]开始执行查询语句sql！')
                return self.cursor.fetchall()
            else:
                print("[SQL]开始执行非查询语句sql！")
                self.conn.commit()
                print(f"[SQL]√执行成功，影响行数:{self.cursor.rowcount}")
                return self.cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            print(e)

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print('[SQL]全部执行完毕，关闭数据库连接！')


if __name__ == '__main__':
    infos = NotifyMessage.read_config()['DATABASES_INFO']
    mysqlobject = MysqlClass(infos['server_ip'], infos['server_user'],
                             infos['server_pwd'], infos['server_db'])
    sql_result = mysqlobject.execute_query(infos['sql_sentence_one'])
    print(sql_result)
