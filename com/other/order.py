
from com.interface.base import BaseData
from com.other.conn import revise_yaml


class Order(BaseData):
    def __init__(self):
        super().__init__()

    def re_get_ip(self):
        """
        暂时用不上,解除ip爬取的任务池堵塞信号
        """
        if self.getting_ip_flag:
            return -1
        else:
            self.getting_ip_flag = False

    def pause_check_node(self):
        """
        暂停节点检测，因为所有调离免费ip池请求都得经过他
        所以这就是不分配ip
        """
        # print(self.pause_flag)
        self.pause_flag = True
        # print(self.pause_flag)

    def continue_check_node(self):
        """
        恢复检查节点
        """
        self.pause_flag = False

    def get_all_acting_ip(self):
        """
        获取免费池内所有可用ip
        """
        return self.sql.select_data()

    def revise_api(self, _url):
        """
        修改IPAPI
        """
        revise_yaml(f"IPAPI: {_url}", self.read()['Label']['IPAPI'])

    def revise_AGlevel(self, _grade: int):
        """
        修改AGlevel
        """
        revise_yaml(f"AGlevel: {_grade}", self.read()['Label']['AGlevel'])

    def get_AGlevel(self):
        """
        读取AGlevel等级
        """
        return self.read()["AGlevel"]

    def flash_all_yaml(self):
        """
        刷新所有读取到的yaml变量,内嵌函数方法
        """
        self.flash_AGlevel()
        self.flash_api_url()
