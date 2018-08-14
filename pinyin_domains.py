# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午1:56
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : pinyin_domains.py
# @Software: PyCharm


import os
import datetime

# 检查query.txt是否存在
if not os.path.exists('resource/query.txt'):
    # 调用系统命令行来创建文件
    os.system(r"touch {}".format('query.txt'))

def getPinyinDomains():
    # 保存正在查询的domains
    domains = []

    # 输入domain后缀
    domain_extension = input("请输入domain后缀，比如：com ")
    # 输入拼音的个数：1单拼 2双拼 3三拼 4四拼
    pinyin_count = int(input("请输入拼音的个数：1单拼 2双拼 3三拼 4四拼"))
    if pinyin_count <= 0:
        pinyin_count = 2
    # 输入包含的关键字
    keycontained = str(input("请输入需要包含的关键字，如果不需要关键字回车即可(不允许包含:空格及其他特殊字符):"))
    # 输入包含的关键字的类型，1是匹配第一个拼音； 2是匹配中间的拼音； 3是拼配结尾的拼音
    keycontainedType = int(input("请选择包含的关键字的类型，1是匹配第一个拼音； 2是匹配中间的拼音； 3是拼配结尾的拼音"))

    with open('resource/pyim-bigdict.txt', 'r+') as f:
        # 读取所有拼音
        lines = f.readlines()
        print('拼音数据准备中，预计有%s个拼音需要处理' % len(lines))
        lines = lines[0:20000]  # 先查5000个

        with open('resource/query.txt', 'a+') as queryFile:
            # 记录时间
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(current_time)
            queryFile.write(current_time)

            # 组合单词为用户输入的domain
            for line in lines:  # reversed(lines): # 倒序遍历
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
                    newlist = list
                    if len(list) > 3:
                        newlist = list[0:pinyin_count]
                    new_line = ''
                    pinyinIdx = 0
                    qualifiedDomain = True
                    for pinyin in newlist:
                        # 根据包含的关键字的类型过滤
                        if keycontainedType == 1:
                            # 1是匹配第一个拼音
                            if pinyinIdx == 0 and pinyin != keycontained:
                                # 不符合就停止
                                qualifiedDomain = False
                                break
                        elif keycontainedType == 2:
                            # 中间的拼音
                            if pinyinIdx > 0 and pinyinIdx < len(newlist) - 1:
                                if pinyin != keycontained:
                                    qualifiedDomain = False
                                    break
                        elif keycontainedType == 3:
                            # 结尾匹配
                            if pinyinIdx == len(newlist) - 1:
                                if pinyin != keycontained:
                                    qualifiedDomain = False
                                    break
                        new_line += pinyin
                        pinyinIdx += 1
                    if qualifiedDomain == True:
                        line = new_line
                    else:
                        continue

                    # 根据keycontained关键字筛选, 不包含关键字的过滤掉
                    if len(keycontained) and keycontained not in line:
                        continue
                else:
                    continue
                if len(line):
                    domain_name = line + "." + domain_extension
                else:
                    continue
                if domain_name not in domains:
                    domains.append(domain_name)
                    queryFile.write(domain_name + '\n')
        return domains

