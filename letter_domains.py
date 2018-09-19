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
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        # 笛卡尔积
        # 创建一个迭代器，生成表示item1，item2等中的项目的笛卡尔积的元组，repeat是一个关键字参数，指定重复生成序列的次数。
        list = itertools.product(alphabet, repeat=4)
        for i in list:
            domain_name = "".join(i) + "." + domain_extension
            domains.append(domain_name)
            domain_name += "\n"
            f.writelines(domain_name)
        return domains

