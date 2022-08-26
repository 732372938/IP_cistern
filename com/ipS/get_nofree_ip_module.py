import re
import threading
import time

import requests

from com.interface.base import BaseData


class GetNoFreeIp(BaseData):
    def __init__(self):
        super().__init__()
        self.time_kill = []
        self.http_ip = None  # 最新IP
        self.http_ip_port = None  # 最新端口
        self.__spend_time = 0

    def time_kill_thread(self, _time=5):
        _count = 0
        while _count < 2:
            time.sleep(_time)
            self.__spend_time += _time
            try:
                # proxies = {
                #     'http': self.http_ip_port,
                #     'https': self.http_ip_port
                # }
                # requests.get("https://api.m.jd.com/", proxies=proxies,
                #              headers=self.user_agent, timeout=10, verify=False).close()
                second = self.ping(self.http_ip, unit='ms', timeout=5)
                # print(second)
                if second and second > 1000.0:
                    self.time_kill.clear()
                    # print(self.http_ip, "挂了")
                    break
                elif not second:
                    self.time_kill.clear()
                    _count += 1
                elif second:
                    # 证明存活
                    if _count > 0:
                        _count -= 1
            except Exception:
                self.time_kill.clear()
                break
        self.time_kill.clear()  # 保底清空

    def get_nofree(self, url=None):
        """
        返回txt 格式：
        27.153.5.211:22271
        只支持单个
        不支持并发检测
        """
        try:
            self.flash_api_url()  # 重新读取文件内容
            if self.time_kill:
                return self.time_kill[0]

            if url is None:
                url = self.api_url
                if not url:
                    return -1

            if not self.time_kill:
                for _url in url:
                    time.sleep(0.8)
                    reps = requests.get(_url,
                                        headers=self.user_agent, verify=False, timeout=20)
                    if reps.status_code != 200:
                        continue
                    # 设置编码
                    reps.encoding = "utf-8"
                    re1 = reps.text
                    # 正则表达式
                    # 分别是IP，端口，类型，国家
                    re_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
                    re_port = re.compile(r':(\d{2,6})')
                    self.http_ip = re_ip.findall(re1)[0]
                    http_port = re_port.findall(re1)[0]
                    self.http_ip_port = self.http_ip + ':' + http_port
                    if not self.time_kill:
                        self.time_kill.append("{}://{}:{}".format("http", self.http_ip, http_port))
                        t = threading.Thread(target=self.time_kill_thread)
                        t.start()
                        return self.time_kill[0]
                    else:
                        return -1
                return -1  # 全部跳出循环，不出结果
            else:
                return self.time_kill[0]

        except Exception as e:
            self.log_write(
                "异常问题，com-->ipS-->get_nofree.py: " + f'<em style="color: rgb(255, 0, 0); font-weight: bolder">{str(e)}</em>')
            return -1
