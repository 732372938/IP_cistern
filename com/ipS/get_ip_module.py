import json
import re
import time

import requests

from com.interface.base import BaseData
from com.detect.proxynova_scraper import get_proxies, get_proxies_by_country


class GetIp(BaseData):
    def __init__(self):
        super().__init__()

    def get_66ip(self):
        """
        网址测试时候503，暂时留着，等后面复活后使用
        :return:
        """
        try:
            time.sleep(3)
            reps = requests.get("http://www.66ip.cn/", headers=self.user_agent, timeout=20, verify=False)
            # 设置编码
            reps.encoding = "utf-8"
            re1 = reps.text
            # 保存到文件
            # 正则表达式
            re_ip = re.compile(r'<tr>\n?<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\n?<td>')
            re_port = re.compile(r'</td>\n?<td>(\d{2,6})</td>\n?<td>')
            http_ip = re_ip.findall(re1)
            http_port = re_port.findall(re1)
            # print(http_ip)
            # print(http_port)
            # print(len(http_ip))
            # print(len(http_port))
            for i in range(len(http_ip)):
                # self.sql.insert_data([http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i]], 'filter')
                self.add_filter_data(http_ip[i] + ':' + http_port[i],
                                     [http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i], "http"])
        except Exception as e:
            self.log_write(
                "异常问题,com-->ipS-->get_ip_module.py-->get_66ip: " + f'{str(e)}')

    def get_crape(self):
        try:
            reps = requests.get("https://api.proxyscrape.com/?request=displayproxies",
                                headers=self.user_agent, timeout=20, verify=False)
            # 设置编码
            reps.encoding = "utf-8"
            re1 = reps.text

            # 正则表达式
            # 分别是IP，端口，类型，国家
            re_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):')
            re_port = re.compile(r':(\d{2,8})')
            http_ip = re_ip.findall(re1)
            http_port = re_port.findall(re1)
            for i in range(len(http_ip)):
                # self.sql.insert_data([http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i]], 'filter')
                self.add_filter_data(http_ip[i] + ':' + http_port[i], [http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i], "http", "EU"])
        except Exception as e:
            self.log_write(
                "异常问题，com-->ipS-->get_ip_module.py-->get_crape: " + f'{str(e)} 国内异常不用管，国外服务器用的')

    def get_github(self):
        try:
            urllist = {
                "http": [
                    "https://raw.iqiq.io/ShiftyTR/Proxy-List/master/http.txt",
                    "https://raw.iqiq.io/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
                    "https://raw.iqiq.io/UptimerBot/proxy-list/main/proxies/http.txt",
                    "https://raw.iqiq.io/UptimerBot/proxy-list/main/proxies_anonymous/http.txt",
                    "https://raw.iqiq.io/saisuiu/uiu/main/cnfree.txt",
                    "https://raw.iqiq.io/saisuiu/uiu/main/free.txt",
                    "https://raw.iqiq.io/TheSpeedX/PROXY-List/master/http.txt",
                    "https://raw.iqiq.io/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
                    "https://raw.iqiq.io/RX4096/proxy-list/main/online/http.txt",
                    "https://raw.iqiq.io/MuRongPIG/Proxy-Master/main/http.txt",
                    "https://raw.iqiq.io/saschazesiger/Free-Proxies/master/proxies/http.txt",
                    "https://raw.iqiq.io/proxy4parsing/proxy-list/main/http.txt",

                ],
                "https": [
                    "https://raw.iqiq.io/ShiftyTR/Proxy-List/master/https.txt",
                    "https://raw.iqiq.io/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
                    "https://raw.iqiq.io/RX4096/proxy-list/main/online/https.txt",
                ],

            }
            for _type in urllist.keys():
                for url in urllist[_type]:
                    time.sleep(10)
                    reps = requests.get(url,
                                        headers=self.user_agent, verify=False, timeout=20)
                    # 设置编码
                    reps.encoding = "utf-8"
                    re1 = reps.text
                    # 正则表达式
                    # 分别是IP，端口，类型，国家
                    re_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
                    re_port = re.compile(r':(\d{2,6})')
                    http_ip = re_ip.findall(re1)
                    http_port = re_port.findall(re1)
                    # print(http_ip)
                    # print(http_port)
                    # print(len(http_ip))
                    # print(len(http_port))
                    for i in range(len(http_ip)):
                        # http_ip_type = "https" if url.split('/')[-1] == "https.txt" else "http"
                        # 创建字典，里面存放所有网络协议,原因https 不能使用,但是转换成http协议可以使用
                        # self.sql.insert_data(
                        #     [http_ip[i] + ':' + http_port[i], http_ip[i], int(http_port[i]), http_ip_type,
                        #      "Github"], 'filter')
                        self.add_filter_data(http_ip[i] + ':' + http_port[i],
                                             [http_ip[i] + ':' + http_port[i], http_ip[i],
                                              int(http_port[i]), _type, "Github"])
        except Exception as e:
            self.log_write(
                "异常问题,com-->ipS-->get_ip_module.py-->get_github: " + f'{str(e)}')

    def get_ip3366(self):
        try:
            for j in range(1, 10):
                try:
                    reps = requests.get(f"https://proxy.ip3366.net/free/?action=china&page={j}",
                                        headers=self.user_agent,
                                        timeout=20, verify=False)
                    # 设置编码
                    reps.encoding = "utf-8"
                    re1 = reps.text

                    # 正则表达式
                    # 分别是IP，端口，类型，国家
                    re_ip = re.compile(r'<td data-title="IP">(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>')
                    re_port = re.compile(r'<td data-title="PORT">(\d{2,6})</td>')
                    http_ip = re_ip.findall(re1)
                    http_port = re_port.findall(re1)
                    for i in range(len(http_ip)):
                        # self.sql.insert_data([http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i]], 'filter')
                        self.add_filter_data(http_ip[i] + ':' + http_port[i],
                                             [http_ip[i] + ':' + http_port[i], http_ip[i],
                                              http_port[i], "http"])
                except Exception as e:
                    return 0
        except Exception as e:
            self.log_write(
                "异常问题,com-->ipS-->get_ip_module.py-->get_ip_module-->get_ip3366: " + f'{str(e)}')

    def get_jxl(self):
        """
        取消了地理位置，全部定义为国内CN
        :return:
        """
        try:
            reps = requests.get("https://ip.jiangxianli.com/?page=1", headers=self.user_agent, timeout=20,
                                verify=False)
            # 设置编码
            reps.encoding = "utf-8"
            re1 = reps.text

            # 正则表达式
            # 分别是IP，端口，类型，国家
            re_ip = re.compile(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>')
            re_port = re.compile(r'<td>(\d{2,6})</td>')
            # re_country = re.compile(r'&quot;country&quot;: &quot;(\w+)')
            re_type = re.compile(r'<td>([HTPSCOK45]{4,6})</td>')

            http_ip = re_ip.findall(re1)
            http_port = re_port.findall(re1)
            # http_country = re_country.findall(re1)
            http_type = re_type.findall(re1)
            for i in range(len(http_ip)):
                # 转成小写
                http_type[i] = http_type[i].lower()
                # 创建字典，里面存放所有网络协议,原因https 不能使用,但是转换成http协议可以使用
                if http_type[i] == "https" or http_type[i] == "http":
                    http_ip_type = {"http": "http", "https": "http", "socks": "socks", "socks4": "socks4",
                                    "socks5": "socks5"}
                    # self.sql.insert_data(
                    #     [http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i], http_ip_type[http_type[i]]],
                    #     'filter')
                    self.add_filter_data(http_ip[i] + ':' + http_port[i],
                                         [http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i],
                                          http_ip_type[http_type[i]]])
        except Exception as e:
            self.log_write(
                "异常问题,com-->ipS-->get_ip_module.py-->get_jiangxianli: " + f'{str(e)}')

    def get_kuai(self):
        try:
            for i in range(1, 3):
                for j in range(1, 11):
                    try:
                        reps = requests.get(f"http://www.kxdaili.com/dailiip/{i}/{j}.html", headers=self.user_agent,
                                            timeout=20, verify=False)
                        # 设置编码
                        reps.encoding = "utf-8"
                        re1 = reps.text
                        # 正则表达式
                        # 分别是IP，端口，类型，国家
                        re_ip = re.compile(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>')
                        re_port = re.compile(r'<td>(\d{2,6})</td>')

                        http_ip = re_ip.findall(re1)
                        http_port = re_port.findall(re1)
                        for v in range(len(http_ip)):
                            # self.sql.insert_data([http_ip[v] + ':' + http_port[v], http_ip[v], http_port[v]],
                            # 'filter')
                            self.add_filter_data(http_ip[i] + ':' + http_port[i],
                                                 [http_ip[v] + ':' + http_port[v], http_ip[v],
                                                  http_port[v], "http"])
                    except Exception as e:
                        return 0
        except Exception as e:
            self.log_write(
                "异常问题,com-->ipS-->get_ip_module.py-->get_kxdaili: " + f'{str(e)}')

    def get_proxydb(self):
        """
        获取代理池的代理，爬取所有国家
        :return:
        """

        def get_list():
            """
            获取这个代理池国家列表，爬取所有国家
            :return: 返回数组
            """
            try:
                country = requests.get("http://www.proxydb.net/", headers=self.user_agent, timeout=20, verify=False)
                country.encoding = "utf-8"
                re1 = country.text
                re_country = re.compile(r'<option value="([A-Z]{2})">.*?\([1-9]\d*\)</option>')
                http_country = re_country.findall(re1)
                return http_country
            except Exception as e:
                self.log_write(
                    "异常问题,com-->ipS-->get_ip_module.py-->get_ip_module.py-->get_proxydb-->get_list: " + f'{str(e)}')
                return []

        try:
            lists = get_list()
            for j in lists:
                time.sleep(5)
                reps = requests.get(f"http://proxydb.net/?country={j}", headers=self.user_agent, timeout=20,
                                    verify=False)
                # 设置编码
                reps.encoding = "utf-8"
                re1 = reps.text
                # 保存到文件
                # 正则表达式
                re_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):')
                re_port = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:(\d{2,6})</a>')
                re_type = re.compile(r'<td>\s*([HTPSCOK45]{4,6})\s*</td>')
                #
                http_ip = re_ip.findall(re1)
                http_port = re_port.findall(re1)  # :80</a>
                http_type = re_type.findall(re1)
                for i in range(len(http_ip)):
                    # 把字母转换为小写
                    http_type[i] = http_type[i].lower()
                    if http_type[i] == "http" or http_type[i] == "https":
                        # self.sql.insert_data([http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i], http_type[
                        # i]], 'filter')
                        self.add_filter_data(http_ip[i] + ':' + http_port[i],
                                             [http_ip[i] + ':' + http_port[i], http_ip[i],
                                              http_port[i], http_type[i]])
        except Exception as e:
            self.log_write(
                "异常问题,com-->ipS-->get_ip_module.py-->get_proxydb.py: " + f'{str(e)}')

    def get_fate(self):
        try:
            reps = requests.get("http://proxylist.fatezero.org/proxy.list", headers=self.user_agent, timeout=20,
                                verify=False)
            # 设置编码
            reps.encoding = "utf-8"
            re1 = reps.text

            # 正则表达式
            # 分别是IP，端口，类型，国家
            re_ip = re.compile(r'"host":\s?"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"')
            re_port = re.compile(r'"port":\s?(\d{2,9})')
            re_country = re.compile(r'"country":\s?"(\w+)"')
            re_type = re.compile(r'"type":\s?"(\w+)"')

            http_ip = re_ip.findall(re1)
            http_port = re_port.findall(re1)
            http_country = re_country.findall(re1)
            http_type = re_type.findall(re1)
            for i in range(len(http_ip)):
                # 创建字典，里面存放所有网络协议,原因https 不能使用,但是转换成http协议可以使用
                if http_type[i] == "https" or http_type[i] == "http":
                    http_ip_type = {"http": "http", "https": "http", "socks": "socks", "socks4": "socks4",
                                    "socks5": "socks5"}
                    # self.sql.insert_data(
                    #     [http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i], http_ip_type[http_type[i]],
                    #      http_country[i]], 'filter')
                    self.add_filter_data(http_ip[i] + ':' + http_port[i],
                                         [http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i],
                                          http_ip_type[http_type[i]],
                                          http_country[i]])
        except Exception as e:
            self.log_write(
                "异常问题,com-->ipS-->get_ip_module.py-->get_kxdaili.py: " + f'{str(e)}')

    def get_proxynova(self, area="CN"):
        """
        不能使用直接异常 Browser closed unexpectedly:
        :param area:
        :return:
        """
        try:
            if area == ' ':
                proxies = get_proxies()
            else:
                proxies = get_proxies_by_country("CN")
            if len(proxies) <= 3:
                return self.get_proxynova(' ')
            for i in range(len(proxies)):
                # self.sql.insert_data([proxies[i].get('proxyIp') + ':' + proxies[i].get('proxyPort'),
                #                       proxies[i].get('proxyIp'),
                #                       proxies[i].get('proxyPort'), "http",
                #                       proxies[1].get('proxyCountry')], 'filter')
                self.add_filter_data(proxies[i].get('proxyIp') + ':' + proxies[i].get('proxyPort'),
                                     [proxies[i].get('proxyIp') + ':' + proxies[i].get('proxyPort'),
                                      proxies[i].get('proxyIp'),
                                      proxies[i].get('proxyPort'), "http",
                                      proxies[1].get('proxyCountry')])

        except Exception as e:
            self.log_write(
                "异常问题,com-->ipS-->get_ip_module.py-->get_proxynova: " + f'{str(e)}')

    def get_pzz(self):
        try:
            reps = requests.get("https://pzzqz.com/", headers=self.user_agent, timeout=20, verify=False)
            # 设置编码
            reps.encoding = "utf-8"
            re1 = reps.text
            # 保存到文件
            # 正则表达式
            # 分别是IP，端口，类型，国家
            re_ip = re.compile(r'<tr>\n?<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\n?<td>')
            re_port = re.compile(r'</td>\n?<td>(\d{2,6})</td>\n?<td class="country">')
            re_country = re.compile(
                r'<span class=".*?"></span>\n?([A-Z].*?)\n?</td>\n?<td class="d-none d-sm-table-cell">')
            re_type = re.compile(r'</div>\n?</div>\n?</td>\n?<td>(\w+)</td>\n?<td class="d-none d-sm-table-cell">')
            #
            http_ip = re_ip.findall(re1)
            http_port = re_port.findall(re1)
            http_country = re_country.findall(re1)
            http_type = re_type.findall(re1)
            for i in range(len(http_ip)):
                # 创建字典，里面存放所有网络协议,原因https 不能使用,但是转换成http协议可以使用
                if http_type[i] == "https" or http_type[i] == "http" or http_type[i] == "Https" or http_type[
                    i] == "Http":
                    http_ip_type = {"http": "http", "Http": "http", "https": "http", "Https": "http", "socks": "socks",
                                    "Socks": "socks", "Socks4": "socks4", "socks4": "socks4",
                                    "socks5": "socks5", "Socks5": "socks5"}
                    # self.sql.insert_data(
                    #     [http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i], http_ip_type[http_type[i]],
                    #      http_country[i]], 'filter')
                    self.add_filter_data(
                        http_ip[i] + ':' + http_port[i],
                        [http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i], http_ip_type[http_type[i]],
                         http_country[i]])
        except Exception as e:
            self.log_write(
                "异常问题,com-->ipS-->get_ip_module.py-->get_pzzqz.py: " + f'{str(e)}')

    def get_scan(self):
        """
        不管什么类型都转换成http协议
        :return:
        """
        try:
            reps = requests.get("https://www.proxyscan.io/", headers=self.user_agent, timeout=20, verify=False)
            # 设置编码
            reps.encoding = "utf-8"
            re1 = reps.text
            # 保存到文件
            # 正则表达式
            # 分别是IP，端口，类型，国家
            re_ip = re.compile(r'<th scope="row">(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</th>')
            re_port = re.compile(r'<td>(\d{2,6})</td>')
            re_country = re.compile(r'<td><span class="flag-icon .*?"></span>\s*(.*?)\s*</td>', re.S)
            # re_type = re.compile(r'<td>\s*([A-Z4-5,</span>]+)\s*</td>', re.S)
            #
            http_ip = re_ip.findall(re1)
            http_port = re_port.findall(re1)
            http_country = re_country.findall(re1)
            # http_type = re_type.findall(re1)
            for i in range(len(http_ip)):
                # 不管什么类型都写入http协议
                # http_ip_type = {"http": "http", "Http": "http", "HTTP": "http", "https": "http", "Https": "http", "HTTPS": "http", "socks": "socks", "Socks": "socks", "SOCKS": "socks", "Socks4": "socks4", "socks4": "socks4",
                #                 "SOCKS4": "socks4", "socks5": "socks5", "Socks5": "socks5", "SOCKS5": "socks5"}
                # self.sql.insert_data([http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i], 'http',
                #                       http_country[i]], 'filter')
                self.add_filter_data(
                    http_ip[i] + ':' + http_port[i],
                    [http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i], 'http',
                     http_country[i]])
        except Exception as e:
            self.log_write(
                "异常问题，com-->ipS-->get_ip_module.py-->get_scan: " + f'{str(e)}')

    def get_v1(self):
        try:
            reps = requests.get("https://www.proxy-list.download/api/v1/get?type=http", headers=self.user_agent,
                                timeout=20, verify=False)
            # 设置编码
            reps.encoding = "utf-8"
            re1 = reps.text

            # 正则表达式
            # 分别是IP，端口，类型，国家
            re_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):')
            re_port = re.compile(r':(\d{2,6})')
            http_ip = re_ip.findall(re1)
            http_port = re_port.findall(re1)
            for v in range(len(http_ip)):
                # self.sql.insert_data([http_ip[v] + ':' + http_port[v], http_ip[v], http_port[v]], 'filter')
                self.add_filter_data(
                    http_ip[v] + ':' + http_port[v],
                    [http_ip[v] + ':' + http_port[v], http_ip[v], http_port[v], "http"])
        except Exception as e:
            self.log_write(
                "异常问题，com-->ipS-->get_ip_module.py-->get_v1: " + f'{str(e)}')

    def get_git_ip(self):
        try:
            reps = requests.get("https://hub.0z.gs/fate0/proxylist/blob/master/proxy.list", headers=self.user_agent,
                                verify=False, timeout=20)
            # 设置编码
            reps.encoding = "utf-8"
            re1 = reps.text

            # 正则表达式
            # 分别是IP，端口，类型，国家
            re_ip = re.compile(r'host&quot;: &quot;(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
            re_port = re.compile(r'&quot;port&quot;: (\d{2,6})')
            re_country = re.compile(r'&quot;country&quot;: &quot;(\w+)')
            re_type = re.compile(r'&quot;type&quot;: &quot;(\w+)')

            http_ip = re_ip.findall(re1)
            http_port = re_port.findall(re1)
            http_country = re_country.findall(re1)
            http_type = re_type.findall(re1)
            for i in range(len(http_ip)):
                # 创建字典，里面存放所有网络协议,原因https 不能使用,但是转换成http协议可以使用
                if http_type[i] == "https" or http_type[i] == "http":
                    http_ip_type = {"http": "http", "https": "http", "socks": "socks", "socks4": "socks4",
                                    "socks5": "socks5"}
                    # self.sql.insert_data(
                    #     [http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i], http_ip_type[http_type[i]],
                    #      http_country[i]], 'filter')
                    self.add_filter_data(
                        http_ip[i] + ':' + http_port[i],
                        [http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i], http_ip_type[http_type[i]],
                         http_country[i]])
        except Exception as e:
            self.log_write(
                "异常问题，com-->ipS-->get_ip_module.py-->git_poxy: " + f'{str(e)}')

    def get_uu_proxy(self):
        """
        爬取的IP池地址
        :return:
        """
        # 获取网站数据
        url = 'https://uu-proxy.com/api/free'
        try:
            strhtml = requests.get(url, headers=self.user_agent, verify=False, timeout=20)
            data = json.loads(strhtml.text)
            for i in range(len(data['free']['proxies'])):
                # 下面是 地址、端口号、协议、支持HTTPS
                ip = data['free']['proxies'][i]['ip']
                port = data['free']['proxies'][i]['port']
                protocol = data['free']['proxies'][i]['scheme']
                country = "CN"
                if protocol == "http" or protocol == "https":
                    # 添加的数据库
                    # self.sql.insert_data([ip + ':' + str(port), ip, str(port), protocol, country], 'filter')
                    self.add_filter_data(
                        ip + ':' + str(port),
                        [ip + ':' + str(port), ip, str(port), protocol, country])
            # 关闭爬取网站
            strhtml.close()
        except Exception as e:
            self.log_write(
                "异常提示,com-->ipS-->get_ip_module.py-->ip_pool.py: " + f'{str(e)}')
