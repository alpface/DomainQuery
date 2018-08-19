# -*- coding: utf-8 -*-
# @Time    : 2018/8/19 上午10:05
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : wordlist_repeat_domain.py
# @Software: PyCharm

def getRepeatWordlist():
    # 保存需要查询的domains
    domains = []

    # 输入domain的后缀
    domain_extension = input("请输入domain后缀，比如：com ")

    with open('resource/wordlist.txt', 'r+') as f:
        # 读取所有单词
        lines = f.readlines()
        # 将单词与domain后缀组合在一起
        for line in lines:
            if '\n' in line:
                # 去掉换行符
                line = line.strip('\n')
            if '-' in line or ' ' in line:
                continue

            if len(line) > 4:
                continue
            # 将单词重复拼接
            word = line + line
            if len(word):
                domain_name = word + "." + domain_extension
            else:
                continue
            if domain_name not in domains:
                domains.append(domain_name)

        return domains