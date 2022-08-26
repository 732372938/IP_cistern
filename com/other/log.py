import logging
import os

from com.other.conn import read_yaml, read_txt

path = read_yaml()['log']

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关
log_file_abs = path
stream_handler = logging.StreamHandler()  # 日志控制台输出
handler = logging.FileHandler(log_file_abs, mode='a', encoding='UTF-8')  # 日志文件输出
handler.setLevel(logging.DEBUG)
# 控制台输出格式
stream_format = logging.Formatter('[%(asctime)s] : %(message)s')
# 文件输出格式
logging_format = logging.Formatter('[%(asctime)s] : %(message)s')
handler.setFormatter(logging_format)  # 为改处理器handler 选择一个格式化器
stream_handler.setFormatter(stream_format)
if not logger.handlers:
    logger.addHandler(handler)  # 为记录器添加 处理方式Handler
    logger.addHandler(stream_handler)


def login(txt):
    """
    日志
    :param txt: 保存的内容
    :return:
    """
    logger.info(txt)
    del_log()


def del_log():
    # 当文件大于1M时，删除文件
    if os.path.getsize(path) > 1242880:
        os.remove(path)


def rz():
    """
    读取日志文件
    :return: 打印html格式的日志，异常返回-1
    """
    try:
        sun = ''
        yml = read_yaml()
        if yml == -1:
            return -1
        rz1 = read_txt(yml['log'])
        if rz1 == -1:
            return -1
        # 遍历所有行
        for i in rz1:
            # 如果就\n则跳过
            if i == '\n':
                continue
            #  把末尾的\n换成<br>
            j = i.replace('\n', '<br>')
            sun += j
        return sun
    except Exception as e:
        return -1
