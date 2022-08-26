import re

import requests

from com.other.conn import revise_yaml, read_yaml
from com.other.log import login


def country_ip(proxies=None):
    """
    获取国家
    :param proxies: 传输的数据，协议ip和端口,默认为None，获取本机的ip
    :return:
    """
    global ip
    try:
        if proxies is None:
            ip = requests.get("https://ip.tool.lu/", timeout=15, verify=False)
        elif proxies != 1:
            ip = requests.get("https://ip.tool.lu/", proxies=proxies, timeout=15, verify=False)
        iptx = ip.text
        ip.close()
        geography = re.findall(r'归属地:\s*(\w+\s*\w+)\s*', iptx)
        # 判断是否网络不受限制
        # 仅仅是用来判断网络是否受限制，不是判断国家的，因为考虑到香港澳门台湾可以不受网络限制
        limit = ["台湾", "香港", "澳门"]
        # 按空格分割
        geography = geography[0].split(" ")
        # 检测数组中是否包含元素

        if geography[1] in limit:
            return geography[1]
        return geography[0]
    except Exception as e:
        return -1


def country_revise():
    """
    根据国家不同·使用不同的代理池
    :return:
    """
    read = read_yaml()
    coun = country_ip()
    login("你服务器所在国家是 " + f'<b style="color: aqua; font-weight: bolder">{coun}</b>')
    if coun != "中国" and coun != -1:
        revise_yaml("country: 国外", read['Label']['country'])
    else:
        revise_yaml("country: 国内", read['Label']['country'])

