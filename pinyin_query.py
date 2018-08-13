# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午1:56
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : pinyin_query.py
# @Software: PyCharm

import time

from bs4 import BeautifulSoup
import itertools
from urllib.request import urlopen
import os
import urllib

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'
}


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
if not os.path.exists('pinyin_active.txt'):
    # 调用系统命令行来创建文件
    os.system(r"touch {}".format('pinyin_active.txt'))

# 保存正在查询的domains
domains = []

# 输入domain后缀
domain_extension = input("请输入domain后缀，比如：com ")

with open('pyim-bigdict.txt', 'r+') as f:
    # 读取所有拼音
    lines = f.readlines()
    lines = lines[0:5000] # 先查5000个
    # 组合单词为用户输入的domain
    for line in  lines: # reversed(lines): # 倒序遍历
        if '\n' in line:
            # 去掉换行符
            line = line.strip('\n')
        # 先按照空格分割字符串，因为后部分为寓意，只要前部分的拼音
        if ' ' in line:
            list = line.split(' ')
            line = list[0]

        # 由于拼音中每个之间都有'-'，所以这里给裁切掉，目前只查询双拼，所以只要两个个拼音
        if '-' in line:
            list = line.split('-')
            if len(list) > 2:
                line = list[0] + list[1]
            else:
                new_line = ''
                for pinyin in list:
                    new_line += pinyin
                line = new_line
        else:
            continue
        if len(line):
            domain_name = line + "." + domain_extension
        else:
            continue
        if domain_name not in domains:
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

        url = "http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=" + domain_name
        # 在request中添加headers
        request = urllib.request.Request(url, headers=header)
        try:
            query = urlopen(request)
        except Exception as error :
            continue
        response = query.read().decode('utf-8')
        if response is not None:
            soup = BeautifulSoup(response, 'html.parser')
            returncode = soup.returncode
            http_code = '-1'
            if returncode is not None and hasattr(returncode, 'string'):
                http_code = soup.returncode.string.strip()
            soup_key = soup.key
            query_domain = line
            if soup_key is not None and hasattr(soup_key, 'string'):
                query_domain = soup.key.string.strip()
            query_result = '-1'
            if soup.original is not None and hasattr(soup.original, 'string'):
                query_result = soup.original.string.split(":")[0].strip()
        else:
            http_code = '-1'
            query_result = '-1'

        time.sleep(0.5)

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
