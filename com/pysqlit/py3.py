# -*- coding:utf8 -*-
import random
import sqlite3
import time

from com.pysqlit.sqlite_queue import SqliteQueue

from com.other.conn import read_yaml

db_path = read_yaml()["db"]


class IPsql:
    """
    初始化
    """

    def __init__(self):
        self.queue_sql = SqliteQueue(db_path, wait=15)
        self.queue_sql.setDaemon(False)  # 默认为守护线程
        self.queue_sql.start()
        pass
        # self.conn = sqlite3.connect(db_path, timeout=10)
        # self.cursor = self.conn.cursor()

    def create_table(self) -> int:
        """
        创建表
        :return: 成0反-1
        """
        try:
            # 创建表 ip= 服务器ip port=端口 protocol=协议 country=国家，ip不能为空和唯一
            sql = "create table acting(ip_port varchar(20) primary key,ip varchar(15) not null,port int(6) not null,  " \
                  "protocol varchar(6), country varchar(10)) "
            self.queue_sql.register_execute(sql)
            return 0
        except Exception as e:
            return -1

    def insert_data(self, data: list, table_name='acting') -> int:
        """
        插入数据，根据传入的数据类型进行判断，自动选者插入方式
        :param data: 要插入的数据 [ip:port,ip地址,端口,协议,地区],其中协议和地区可以不带
        :param table_name: 表名,默认acting
        :return: 0 or -1
        """
        try:
            if isinstance(data, list):
                # 获取data长度
                long = len(data)
                lis = ['http', 'No']
                # 表示插入值完整不用补充
                if long > 4:
                    sql = f"INSERT INTO {table_name} VALUES ('{data[0]}','{data[1]}',{data[2]},'{data[3]}','{data[4]}')"
                elif long == 4:
                    sql = f"INSERT INTO {table_name} VALUES ('{data[0]}','{data[1]}',{data[2]},'{data[3]}', '{lis[1]}')"
                elif long == 3:
                    sql = f"INSERT INTO {table_name} VALUES ('{data[0]}','{data[1]}',{data[2]}, '{lis[0]}', '{lis[1]}')"
                else:
                    sql = " "
                self.queue_sql.register_execute(sql)
            return 0
        except Exception as e:
            return -1

    def select_data(self, country="Null", surface='acting') -> list:
        """
        查询数据所有
        :param country: 国家, 默认所有
        :param surface: 数据库表名，默认acting
        :return: http或https的代理,反之-1
        """

        global cursor, conn
        try:
            time.sleep(random.uniform(0.8, 1.3))
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # _results = []
            if country != "Null":
                cursor.execute(f"select * from {surface} where country='{country}'")
            else:
                cursor.execute(f"select * from {surface}")
            # 获取查询数据
            _results = cursor.fetchall()
            return _results
        except Exception as e:
            return []
        finally:
            cursor.close()
            conn.close()

    def delete_data(self, ip_port, surface='acting') -> int:
        """
        根据条件删除数据
        :param ip_port: ip:port
        :param surface: 数据库表名，默认acting
        :return: 正常返回0，不正常返回1
        """
        try:
            self.queue_sql.register_execute(f"delete from {surface} where ip_port='{ip_port}'")
            return 0
        except Exception as e:
            return -1

    # 下面是另一个表的
    def del_ti(self, ID) -> int:
        """
        根据条件删除数据
        """
        try:
            self.queue_sql.register_execute(f"delete from ti where ID={ID}")
            return 0
        except Exception as e:
            return -1

    def insert_ti(self, data: list) -> int:
        """
        :return: 0 or -1
        """
        try:
            sql = f"INSERT INTO ti VALUES ({data[0]},'{data[1]}','{data[2]}')"
            print(sql)
            self.queue_sql.register_execute(sql)
            return 0
        except Exception as e:
            print(e)
            return -1

    def query_ti(self) -> list:
        """
        查询数据所有
        """
        global cursor, conn
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # _results = []
            cursor.execute(f"select * from ti order by ID asc")
            # 获取查询数据
            _results = cursor.fetchall()
            return _results
        except Exception as e:
            return []
        finally:
            cursor.close()
            conn.close()
