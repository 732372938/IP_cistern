

from flask import Flask, request, render_template

from com.Web import but
from com.detect.write_file import WriteFile
from com.ipS.get_nofree_ip_module import GetNoFreeIp
from com.other.conn import read_yaml
from com.other.log import rz
from com.other.order import Order
from com.other.tizone import Zone, AS

port = read_yaml()
app = Flask(__name__)
app.register_blueprint(but.app, url_prefix='/')
WF = WriteFile()
Order = Order()
GNF = GetNoFreeIp()
ip_pause_flags = False
ZO = Zone()


@app.route('/', methods=['GET', 'POST'])
def register():
    """停止恢复IP分配"""
    global ip_pause_flags
    mark = ""
    if request.method == 'POST':
        tf = request.form.get('tf')
        urls = request.form.get('url')
        grade = request.form.get('grade')
        if urls:
            # 按照空格分隔
            url = urls.split(" ")
            # 如果有空元素去除，防止输入多个空格
            url = [i for i in url if (len(str(i)) != 0)]
            Order.revise_api(url)
            mark += "提交API成功"
        if grade:
            Order.revise_AGlevel(int(grade))
            mark += f"修改检测等级{grade}"
        if tf == "start":
            ip_pause_flags = False
            return render_template('ip.html', ip_pause_flags=ip_pause_flags)
        elif tf == "stop":
            ip_pause_flags = True
            return render_template('ip.html', ip_pause_flags=ip_pause_flags)
        else:
            return render_template('ip.html',
                                   ip_pause_flags=ip_pause_flags,
                                   msg=mark if len(mark) > 4 else "没有提交任何内容")
    else:
        return render_template('ip.html', ip_pause_flags=ip_pause_flags)


@app.route('/log', methods=['GET'])
def cat_log():
    return rz()


# @app.route('/regetip', methods=['GET'])
# def re_get_ip():
#     Order.get_ip()
#     return "重新爬取ip任务提交成功"


@app.route('/getall', methods=['GET'])
def get_all_ip():
    all = Order.get_all_acting_ip()
    if len(all) > 0:
        return render_template('check.html', name=all)
    else:
        return "没有可用代理"


# @app.route('/api/mod/<_url>', methods=['GET'])
# def revise_api(_url):
#     Order.revise_api(_url)
#     return "提交修改！"


# 接收get请求 /http
@app.route("/http", methods=["GET"])
def http():
    """
    免费代理的接口
    :return: 返回协议://ip:端口
    """

    global ip_pause_flags
    # 判断是否要返回代理
    ti = ZO.compared_ti(AS())
    if ti == 0:
        if ip_pause_flags:
            return 'http://127.0.0.1'
        result = WF.check_node()
        # 若检查不过，返回127.0.0.1
        return result if result != -1 else 'http://127.0.0.1'
    return 'http://127.0.0.1'


@app.route("/nofreehttp", methods=["GET"])
def nofree_http():
    """
    付费代理的接口
    :return: 返回协议://ip:端口
    """
    global ip_pause_flags
    ti = ZO.compared_ti(AS())
    if ti == 0:
        if ip_pause_flags:
            return 'http://127.0.0.1'
        result = GNF.get_nofree()
        # 获取值为-1则调用免费池
        if result == -1:
            result = WF.check_node()
        # 若检查不过，返回127.0.0.1
        return result if result != -1 else 'http://127.0.0.1'
    return 'http://127.0.0.1'


def run_web():
    app.run(
        host='0.0.0.0',
        port=port['port'],
        debug=False
    )
