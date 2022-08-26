import os

from flask import Blueprint, request, render_template

from com.other.tizone import Zone
from com.pysqlit.py3 import IPsql

app = Blueprint('but', __name__)
ZO = Zone()
tise = IPsql()


@app.route('/renew')
def renew():
    os.system("sh gi.sh")
    return "你按下了更新"


@app.route("/ti", methods=['GET', 'POST'])
def ti():
    """
    返回时间列表和添加时间
    :return:
    """
    if request.method == 'POST':
        tis = request.form.get('ti')
        if tis[0] == "删":
            tise.del_ti(tis[1::])
        else:
            ZO.insert_time(tis[1::])
        return render_template('ti.html', name=tise.query_ti())
    else:
        return render_template('ti.html', name=tise.query_ti())
