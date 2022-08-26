import threading
import time

from flask_apscheduler import APScheduler
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

from com.Web.index import run_web
from com.detect.http_re import HttpRe
from com.ipS.get_ip_module import GetIp
from com.other.conn import read_yaml
from com.other.country import country_revise

scheduler = APScheduler()
pool = ThreadPoolExecutor(max_workers=5, thread_name_prefix="get_ip_")
all_task_list = []


class RunMain(GetIp, HttpRe):
    def __init__(self):
        super().__init__()
        self.log_write('<h1 style="color: rgb(111, 255, 0);">===程序开始运行===</h1>')

    def get_ip(self):
        """
        执行爬取
        :return:
        """
        global all_task_list
        if self.getting_ip_flag:
            self.log_write("爬取IP任务池中已有任务，阻断此次任务提交！")
            return
        area = read_yaml()
        all_task_list = []
        self.clear_filter_data()  # 清空数据
        # 获取代理
        ip_db = {
            "get_ip": self.get_uu_proxy,
            "get_git_ip": self.get_git_ip,
            "get_fate": self.get_fate,
            "get_pzz": self.get_pzz,
            "get_scan": self.get_scan,
            "get_kuai": self.get_kuai,
            "get_ip3366": self.get_ip3366,
            "get_v1": self.get_v1,
            "get_jxl": self.get_jxl,
            "get_proxydb": self.get_proxydb,
            # "get_66ip": self.get_66ip,  # 小心被拉黑
            "get_github": self.get_github,
            "get_proxynova": self.get_proxynova,  # 不能使用去方法里面查看异常信息
            "get_crape": self.get_crape  # 适配非国内环境的代理
        }
        for task in ip_db.keys():
            not_included = ["get_crape"]
            # 本身携带异步且有handle的，丢进线程池会有bug
            not_in_pool = ["get_proxynova"]
            if task not in not_included and task not in not_in_pool:
                # print("任务提交:" + task)
                all_task_list.append(pool.submit(ip_db.get(task)))
            if task in not_in_pool:
                # print("任务执行:" + task)
                ip_db.get(task)()

        # 下面是适配非国内环境的代理
        if area['country'] != '国内':
            all_task_list.append(pool.submit(ip_db.get("get_crape")))
        self.log_write("任务已全部提交，开始爬取ip")
        self.getting_ip_flag = True
        t3 = threading.Thread(target=self.check_all_task_list_thread)
        t3.start()
        # wait(all_task_list, return_when=ALL_COMPLETED)
        # 测试代理
        # check_ip()

    def check_all_task_list_thread(self):
        """
        监听线程池任务线程，防止重复提交到任务池
        """
        global all_task_list
        wait(all_task_list, return_when=ALL_COMPLETED)
        self.log_write("爬取ip完毕，休息10min")
        time.sleep(600)
        self.getting_ip_flag = False

    def check_add_ip_thread(self):
        """
        监听添加线程
        """
        self.log_write("监听筛选池线程启动成功")
        count = 1
        while True:
            time.sleep(count)
            # sql = self.sql.select_data(country="Null", surface='filter')
            sql = list(self.filter_data.values()) if self.filter_data else " "
            if type(sql) == list and len(sql) > 0:
                if len(sql) >= 5:
                    self.check_ip()
                    count = 1
            else:
                if count < 15:
                    count = +2

    def check_exist_ip_thread(self):
        """
        监听ip存活线程
        """
        self.log_write("监听ip池存活线程启动成功")
        while True:
            time.sleep(35)  # 太快容易被拉黑
            sql1 = self.sql.select_data()
            if type(sql1) == list:
                if len(sql1) >= 0:
                    self.check_ip("acting")

    def run_main(self):

        @scheduler.task('interval', id='implement', hours=6)
        def implement():
            """
            定时任务 每四小时检测一次大检测
            :return:
            """
            try:
                self.get_ip()
            except Exception as e:
                self.log_write("定时任务报错" + str(e))

        @scheduler.task('interval', id='timing_ck', minutes=2)
        def timing_ck():
            """
            定时任务 每⑤分钟检测一次
            :return:
            """
            # 用来获取数据长度
            sql = self.sql.select_data()
            # 检测返回的类型
            if type(sql) == list and len(sql) > 0:
                # 如果数据长度不大于6条，就重新爬取
                if len(sql) <= 5:
                    self.get_ip()
                else:
                    self.log_write(
                        f'ip数据还有<b style="color: rgb(255, 0, 255); font-weight: bolder">{len(sql)}条</b>, 不需要重新爬取')
            else:
                self.log_write("数据库中没有数据，重新爬取")
                self.get_ip()

        # 判断是否是国外环境以此来决定是否爬取国外代理池
        country_revise()
        timing_ck()
        scheduler.start()
        t1 = threading.Thread(target=self.check_add_ip_thread)
        t2 = threading.Thread(target=self.check_exist_ip_thread)
        t1.start()
        t2.start()


if __name__ == '__main__':
    RunMain().run_main()
    run_web()
