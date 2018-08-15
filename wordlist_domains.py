# -*- coding: utf-8 -*-
# @Time    : 2018/8/9 下午11:24
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : wordlist_domains.py
# @Software: PyCharm


import os


# 检查query.txt是否存在
if not os.path.exists('resource/query.txt'):
    # 调用系统命令行来创建文件
    os.system(r"touch {}".format('resource/query.txt'))


def getWordListDomains():
    # 保存正在查询的domains
    domains = []

    # 输入domain后缀
    domain_extension = input("请输入domain后缀，比如：com ")

    with open('resource/wordsEn.txt', 'r+') as f:
        # 读取所有单词
        lines = f.readlines()
        # 组合单词为用户输入的domain
        for line in lines:  # reversed(lines): # 倒序遍历
            if '\n' in line:
                # 去掉换行符
                line = line.strip('\n')
            if '-' in line:
                # 分割-
                list = line.split('-')
                line = list[0]
            # 如果有空格，且低于15未的，剪切掉空格
            if ' ' in line:
                if domain_extension == 'com':
                    if len(line) <= 7:
                        line = line.replace(' ', '')
                    else:
                        continue
                else:
                    continue
            if len(line) > 5 and domain_extension != 'com':
                continue
            if len(line):
                domain_name = line + "." + domain_extension
            else:
                continue
            if domain_name not in domains:
                domains.append(domain_name)

        return domains
