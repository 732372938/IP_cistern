import re
from datetime import datetime
from datetime import timedelta
from datetime import timezone


from com.pysqlit.py3 import IPsql


ti = IPsql()


def AS():
    """
    获取当前时间中国时区的时间
    :return:
    """
    SHA_TZ = timezone(
        timedelta(hours=8),
        name='Asia/Shanghai',
    )
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    beijing_now = utc_now.astimezone(SHA_TZ)
    return beijing_now.strftime('%H:%M:%S')


class Zone:
    """
    和插入时间有关的
    """

    def __init__(self):
        super().__init__()

    def insert_time(self, txt: str):
        """
        插入
        :param txt: 时:分:秒&阻断秒长
        :return:
        """
        # 判断输入的是否符合要求
        tie = re.findall(r"([0-1][0-9]:[0-6][0-9]:[0-6][0-9])&(\d+)", txt)
        if tie:
            sun = ti.query_ti()
            s = 0
            for i in sun:
                if i[0] != s:
                    break
                else:
                    s += 1
            if sun == len(sun):
                s += 1
            ti.insert_ti([s, tie[0][0], tie[0][1]])
            return 0
        return -1

    def convert_ti(self, tis:str):
        """
        把时间转换成秒
        :param tis: 时:分:秒
        :return: 返回秒
        """
        h, m, s = tis.strip().split(':')  # .split()函数将其通过':'分隔开，.strip()函数用来除去空格
        second = int(h) * 3600 + int(m) * 60 + int(s)  # int()函数转换成整数运算
        return second

    def compared_ti(self, tis):
        """
        对比是否为不用代理时间
        :param: tis: 传递过来的时间
        :return: 在不放代理时间返回-1，否则0
        """
        nowti = self.convert_ti(tis)
        # 获取时间
        record = ti.query_ti()
        for i in record:
            # 把数据库里的转换成秒
            reco = self.convert_ti(i[1])
            # 获取延迟秒
            recoadd = int(reco) + int(i[2])
            if reco <= nowti <= recoadd:
                # 符合条件返回
                return -1
        return 0

