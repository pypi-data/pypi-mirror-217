import os
import re
import time
import uuid

from pathlib import Path

from dateutil import parser
from dateutil.relativedelta import relativedelta

SERVICE = 'API'


def project_dir():
    root = os.getenv('PROJECT_DIR')
    if root is None:
        return '/service/app'

    return root


def to_dict(**kwargs):
    """
    转化为dict类型数据
    :param kwargs:
    :return:
    """
    return kwargs


def to_list(*args):
    """
    转化为list类型数据
    :param args:
    :return:
    """
    return args


def extract_digit(s: str):
    """
    提取字符串中所有数字
    :param s:
    :return:
    """
    return "".join(list(filter(str.isdigit, s)))


def time_add(dt: str, years: int = 0, months: int = 0, days: int = 0,
             hours: int = 0, minutes: int = 0, seconds: int = 0):
    """
    时间加法器
    :param dt:
    :param years:
    :param months:
    :param days:
    :param hours:
    :param minutes:
    :param seconds:
    :return:
    """
    t = parser.parse(dt)
    t = t + relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds)

    return t.strftime('%Y-%m-%d %H:%M:%S')


def time_diff(dt1: str, dt2: str):
    """
    时间差
    :param dt1:
    :param dt2:
    :return: 秒
    """
    t1 = parser.parse(dt1)
    t2 = parser.parse(dt2)

    return (t2 - t1).total_seconds()


def is_valid_url(url: str):
    """
    验证url有效性
    :param url:
    :return:
    """
    regex = r'http[s]?://(?:[a-zA-Z][0-9]|[$-@.&+]|[!*\(\),]|(?:%[0-9a-zA-F]))+'

    p = re.compile(regex)

    if url is None:
        return False

    if re.search(p, url):
        return True

    return False


def replace(content: dict, **kwargs):
    """
    替换字典中变量
    :param content:
    :return:
    """
    ds = str(content)

    for key, value in kwargs.items():
        if type(value) is str:
            ds = ds.replace('#{}'.format(key.upper()), value.replace('\'', '"'))
            ds = ds.replace('*{}'.format(key.upper()), value.replace('\'', '"'))
        else:
            ds = ds.replace('\'#{}\''.format(key.upper()), str(value))
            ds = ds.replace('\'*{}\''.format(key.upper()), str(value))

    return eval(ds)


def gen_sn():
    """
    生成唯一的测试序列号
    :return:
    """
    return uuid.uuid4().hex


def sys_current_time():
    """
    服务器系统时间
    :return:
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def tcp_extract(tcp: str):
    """
    TCP获取ip和port
    :param tcp:
    :return:
    """
    result = re.search("((?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]))", tcp)
    if result:
        return result.group(1), int(tcp.split(':')[2])
    else:
        return "tcp cannot find ip or port"


def exist(project_path, *args):
    """
    目录是否存在
    :param project_path:
    :param args:
    :return:
    """
    file_path = os.path.join(project_path, *args)
    if os.path.exists(file_path):
        return True
    else:
        return False


def makeDir(project_path, *args):
    """
    创建目录
    :param project_path:
    :param args:
    :return:
    """
    dir_path = os.path.join(project_path, *args)
    if not exist(project_path, *args):
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    return dir_path


if __name__ == '__main__':
    print(time.localtime())
    s = time.localtime()
    import datetime

    someday = datetime.datetime.now()
    print(someday.strftime("%Y%m%d%H%M%S%f"))
    print(time.strftime("%Y%m%d%H%M%S", time.localtime()))
