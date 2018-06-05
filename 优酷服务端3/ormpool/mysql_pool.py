import pymysql
from ormpool import db_pool

class Mysql:
    def __init__(self):
        self.conn=db_pool.POOL.connection()
        self.cursor=self.conn.cursor(cursor=pymysql.cursors.DictCursor)
    def close_db(self):
        self.conn.close()
        self.cursor.close()
    def select(self,sql,args=None):
        self.cursor.execute(sql,args)
        res=self.cursor.fetchall()
        return res
    def execute(self,sql,args):
        try:
            self.cursor.execute(sql,args)
            rows=self.cursor.rowcount
            return rows
        except BaseException as a:
            print(a)
        finally:
            self.close_db()