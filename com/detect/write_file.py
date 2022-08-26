"""
请求后用于返回IP处理地方
"""
import random
import time

from com.interface.base import BaseData
from com.other.log import login


class WriteFile(BaseData):
    def __init__(self):
        super().__init__()
        self.last_choice = []

    # 获取节点
    def read_node(self, sql):
        """
        随机IP，为了避免很多人同时使用一个IP
        :param: sql: 数据库类
        :return: 返回协议://ip:端口，如果都不可用返回-1
        """
        sql = sql.select_data()
        randomnum = random.randint(0, len(sql) - 1)
        random_ip = sql[randomnum][3] + "://" + sql[randomnum][0]
        # last_choice.append([random_ip, randomnum])
        return random_ip

    # 添加节点检测
    def check_node(self):
        """
        添加之前再次检测节点是否可用
        获取随机节点
        :return: 返回协议://ip:端口 没有返回-1
        """
        if self.pause_flag:
            login("收到暂停信号，check_node")
            return -1

        sql = self.sql.select_data(country="中国")
        if not sql:
            time.sleep(random.uniform(0.8, 2.8))
            sql = self.sql.select_data(country="中国")
        try:
            # 判断返回的是不是数组
            if isinstance(sql, list):
                # 判断数组长度是否大于3
                if len(sql) > 3:
                    # 第一次使用随机IP，诺随机IP不可用，按顺序获取IP
                    while True:
                        randomnum = random.randint(0, len(sql) - 1)
                        random_ip = sql[randomnum][3] + "://" + sql[randomnum][0]
                        if [random_ip, randomnum] == self.last_choice:
                            continue
                        else:
                            break
                    self.last_choice = [random_ip, randomnum]
                    second = self.ping(sql[randomnum][1], unit='ms', timeout=10)
                    if second and second < 1000.0:
                        return random_ip
                    else:
                        return self.read_node(self.sql)
            # 走到这里说明不复合上面的条件
            return self.read_node(self.sql)
        except Exception as e:
            login("节点池中没有节点代理池可能不能使用了，check_node：" + str(e))
            return -1
