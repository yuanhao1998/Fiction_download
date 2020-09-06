import pymysql

from source_code.settings.dev import PYMYSQL


class Conn:  # 建立pymysql连接与提交
    def __init__(self):
        self.conn = pymysql.connect(**PYMYSQL)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)  # 设置查询的结果为字典，默认为元组

    def execute(self, query, args=None):
        if isinstance(args, list):
            self.cursor.executemany(query, args)
        else:
            self.cursor.execute(query, args)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchmany(self, size=None):
        return self.cursor.fetchmany(size)

    def fetchall(self):
        return self.cursor.fetchall()

    def rollback(self):
        return self.conn.rollback()

    def rowcount(self):
        return self.cursor.rowcount()

    def __del__(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
