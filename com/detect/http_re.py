from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

import requests

from com.interface.base import BaseData
from com.other.country import country_ip


class HttpRe(BaseData):
    def __init__(self):
        super().__init__()
        self.pool = ThreadPoolExecutor(max_workers=200, thread_name_prefix="check_ip_")
        self.all_task_list = []
        self._getting_ip_flag = False
        self.del_ip_list = []  # 怀疑列表（因网络波动造成误判，需二次确认才删除ip）

    def http_request(self, http_ip_port, ip_port, data, sql_name='filter'):
        """
        检测节点是否可用
        :param data:
        :param http_ip_port: 测试的节点
        :param ip_port: 如果不可用删除的索引
        :param sql_name: 扫描的数据库
        :return:
        """
        proxies = {
            'http': http_ip_port,
            'https': http_ip_port
        }
        try:
            check_wb = [
                "https://plogin.m.jd.com/",
                "https://api.m.jd.com/",
                "https://www.jsjiami.com/",
                "https://st.jingxi.com/",
                "https://bean.m.jd.com",
                "http://isvjcloud.com",  # 基本只能是国内代理
            ]
            # 检测节点是否可用.多次检测，如果可用，就把节点添加到字典中，检测多个防止代理无效，主要用于京东使用代理验证京东网址是否支持代理
            # 请求超过3秒，就认为节点不可用
            # print(AGlevel)
            for i in range(0, self.AGlevel):
                r = requests.get(check_wb[i], proxies=proxies, headers=self.user_agent, timeout=20, verify=False)
                if r.status_code != 200:
                    raise ConnectionError
            second = self.ping(data[1], unit='ms', timeout=10)
            if second and second >= 1000.0:
                self.del_filter_data(data[0])
                # print(data[0])
            elif sql_name == 'filter':
                location = country_ip(proxies)
                # 检测成功添加到可用代理的数据库中
                if location != -1:
                    # print(location)
                    self.sql.insert_data([data[0], data[1], data[2], data[3], location])
                    print("提交成功")
                    # self.filter_data.setdefault(data[0], [data[0], data[1], data[2], data[3], location])
                # 删除节点筛选
                # self.sql.delete_data(ip_port, sql_name)
                self.del_filter_data(data[0])
            elif sql_name == 'acting':
                if http_ip_port in self.del_ip_list:
                    # 如果正常了，那就不怀疑了XD
                    self.del_ip_list.remove(http_ip_port)
        except Exception as e:
            # 不做任何输出,删除不可用的节点
            # print("kill-" + sql_name + '-' + http_ip_port)
            if sql_name == 'acting':
                if http_ip_port in self.del_ip_list:
                    self.sql.delete_data(ip_port, sql_name)
                    self.del_ip_list.remove(http_ip_port)
                else:
                    self.del_ip_list.append(http_ip_port)
            elif sql_name == 'filter':
                # self.sql.delete_data(ip_port, sql_name)
                # print(e)
                self.del_filter_data(data[0])

    def check_ip(self, sql_name='filter'):
        """
        使用多线程检测代理IP的可用性
        :param sql_name:
        :return:
        """
        # print(self._getting_ip_flag)
        if not self._getting_ip_flag:
            self.flash_AGlevel()
            if sql_name == "acting":
                sq = self.sql.select_data("Null", sql_name)
            else:
                sq = list(self.filter_data.values())
            # print(sq)
            for i in sq:
                # print(i)
                # t = threading.Thread(target=http_request, args=(i[3] + "://" + i[0], i[0], i, sql_name,))
                self.all_task_list.append(self.pool.submit(self.http_request, i[3] + "://" + i[0], i[0], i, sql_name))
            self._getting_ip_flag = True
            wait(self.all_task_list, return_when=ALL_COMPLETED)
            self.all_task_list = []
            self._getting_ip_flag = False
