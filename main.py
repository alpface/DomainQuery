# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午4:56
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : main.py
# @Software: PyCharm

from pinyin_domains import getPinyinDomains
from letter_domains import getLetterDomains
from wordlist_domains import getWordListDomains
from query_aliyun import domainQueryFromAliyun
from wordlist_repeat_domain import getRepeatWordlist
import time

if __name__=='__main__':
    try:
        # 输入domain后缀
        code = str(input("请输入需要查询的类型: 1(四字母) 2(拼音) 3 (单词) 4（重复单词）"))
        domains = []
        if code == '2':
            domains = getPinyinDomains()
        elif code == '1':
            domains = getLetterDomains()
        elif code == '3':
            domains = getWordListDomains()
        elif code == '4':
            domains = getRepeatWordlist()
        else:
            pass
        if len(domains) == 0:
            pass

        with open('resource/active.txt', 'a+') as activeFile:
            # 记录当前查询日期
            isotimeformat = '%Y-%m-%d %H:%M:%S'
            current_date = time.strftime(isotimeformat, time.localtime(time.time()))
            activeFile.write(current_date + "\n")

        domainQueryFromAliyun(domains)
    except KeyboardInterrupt as e:
        print(e.__str__())

