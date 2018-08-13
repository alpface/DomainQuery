#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import itertools
import os


# 检查query.txt是否存在
if not os.path.exists('resource/query.txt'):
    # 调用系统命令行来创建文件
    os.system(r"touch {}".format('resource/query.txt'))


def getLetterDomains():
    # 保存正在查询的domains
    domains = []

    # 输入domain后缀
    domain_extension = input("请输入domain后缀，比如：com ")

    with open('resource/query.txt', 'a+') as f:
        # 清空query.tex中文内容，也就是上传查询的内容, truncate(0)从第0个字节以后的内容全部删除了
        res = f.truncate(0)

        # 将字母拼接为每一个域名
        for i in itertools.product("abcdefghijklmnopqrstuvwxyz", repeat=4):
            domain_name = "".join(i) + "." + domain_extension
            domains.append(domain_name)
            domain_name += "\n"
            f.writelines(domain_name)
        return domains

