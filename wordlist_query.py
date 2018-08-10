# -*- coding: utf-8 -*-
# @Time    : 2018/8/9 下午11:24
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : wordlist_query.py
# @Software: PyCharm

import time

from bs4 import BeautifulSoup
import itertools
from urllib.request import urlopen
import os

class colors:
    BLACK = '\033[0;30m'
    DARK_GRAY = '\033[1;30m'
    LIGHT_GRAY = '\033[0;37m'
    BLUE = '\033[0;34m'
    LIGHT_BLUE = '\033[1;34m'
    GREEN = '\033[0;32m'
    LIGHT_GREEN = '\033[1;32m'
    CYAN = '\033[0;36m'
    LIGHT_CYAN = '\033[1;36m'
    RED = '\033[0;31m'
    LIGHT_RED = '\033[1;31m'
    PURPLE = '\033[0;35m'
    LIGHT_PURPLE = '\033[1;35m'
    BROWN = '\033[0;33m'
    YELLOW = '\033[1;33m'
    WHITE = '\033[1;37m'
    DEFAULT_COLOR = '\033[00m'
    RED_BOLD = '\033[01;31m'
    ENDC = '\033[0m'

# 检查query.txt是否存在
if not os.path.exists('query.txt'):
    # 调用系统命令行来创建文件
    os.system(r"touch {}".format('query.txt'))

# 检查active.txt是否存在
if not os.path.exists('active.txt'):
    # 调用系统命令行来创建文件
    os.system(r"touch {}".format('active.txt'))

# 保存正在查询的domains
domains = []

# 输入domain后缀
domain_extension = input("请输入domain后缀，比如：com ")

with open('wordlist.txt', 'r+') as f:
    # 读取所有单词
    lines = f.readlines()
    # 组合单词为用户输入的domain
    for line in lines:
        if '\n' in line:
            # 去掉换行符
            line = line.strip('\n')
        # 如果有空格，且低于15未的，剪切掉空格
        if ' ' in line:
            if len(line) <= 15:
                line.replace(' ', '')
            else:
                continue
        domain_name = line + "." + domain_extension
        domains.append(domain_name)


try:
    # 读取所有需要查询的domain
    lines = domains
    for line in lines:
        domain_name = line
        if '\n' in line:
            # 如果domain中包含\n就剪切掉
            domain_name = line.strip('\n')
        # response = requests.get("http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=" + domain_name).content.decode("utf-8")
        query = urlopen("http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=" + domain_name)
        response = query.read().decode('utf-8')
        soup = BeautifulSoup(response, 'html.parser')
        http_code = soup.returncode.string.strip()
        query_domain = soup.key.string.strip()
        query_result = soup.original.string.split(":")[0].strip()

        time.sleep(1)

        if http_code == '200' and query_result == '210':  # domain可以注册
            print(
                colors.YELLOW + "Very nice! domain: %s is available " % query_domain + colors.ENDC)
            # 将可以注册的domain写入到active.txt中
            with open('active.txt', 'a+') as f:
                f.write(query_domain + "\n")

        elif http_code == '200' and query_result == '211':  # domain不可以注册
            print("sory domain: %s is not available" % query_domain)

        elif query_result == '213':  # domain查询超时
            print('domain: %s query timeout' % query_domain)

        else:
            print("that is really bad!")
            print(http_code)
            print(query_domain)
            print(query_result)


except KeyboardInterrupt as e:
    print(e.__str__())
