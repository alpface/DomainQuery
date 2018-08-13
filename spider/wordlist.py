# -*- coding: utf-8 -*-
# @Time    : 2018/8/9 下午10:51
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : wordlist.py
# @Software: PyCharm


import requests
from bs4 import BeautifulSoup
import pymysql
import re

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'
}


def get_urlhtml(url):  # 爬取主页
    try:
        html = requests.get(url, headers=header)  # 使用requests库爬取
        if html.status_code == 200:  # 如果状态码是200，则表示爬取成功
            print(url + '解析成功')
            return html.text  # 返回H5代码
        else:  # 否则返回空
            print('解析失败')
            return None
    except Exception as e:  # 发生异常返回空
        print('解析失败')
        print(e.__str__())
        return None


def get_url(html):  # 解析首页得到所有的网址
    word_all = []  # 所有classid可能取值的列表
    mess = BeautifulSoup(html, 'lxml')
    word_num = mess.select('.main_l li')
    for word in word_num:
        word_all.append(word.get('class_id'))
    return word_all


def paqu_wangye(reponse, name):  # 爬取所有的单词、发音、翻译
    word_mause = {}
    mess = BeautifulSoup(reponse, 'lxml')
    word = mess.find_all('div', class_="word_main_list_w")
    mause = mess.find_all(class_="word_main_list_y")
    fanyi = mess.find_all(class_='word_main_list_s')
    for i in range(1, len(word)):
        key = word[i].span.get('title')
        f = mause[i].strong.string.split()
        y = fanyi[i].span.get('title')
        if len(f) == 0:  # 因为某些发音不存在，我们直接放弃，不存入
            continue
        word_mause[key] = [f[0], y, name]
    print('创建数据成功')
    return word_mause


def paqumusci(reponse):  # 爬取音频
    mause_list = []  # 音频URL列表
    word_list = []  # 单词列表
    mess = BeautifulSoup(reponse, 'lxml')
    mause = mess.find_all(class_="word_main_list_y")
    word = mess.find_all(class_='word_main_list_w')
    for i in range(1, len(mause)):
        word_list.append(word[i].span.get('title'))  # 加入列表
        mause_list.append(mause[i].a.get('id'))  # 加入列表
    for i in range(len(word_list)):  # 存入文件
        try:
            file = open('static//music//' + word_list[i] + '.mp3', 'wb')  # 打开文件，wb打开，以.mp3的格式打开
            flag = requests.get(mause_list[i])  # 爬取音频URL
            file.write(flag.content)  # 以二进制流写入
            file.close()  # 关闭文件
            print(word_list[i] + '存储成功')
        except:
            print(word_list[i] + '存储失败')


def cucun(word_mause):  # 爬取数据到数据库
    # 解决UnicodeEncodeError: 'latin-1' codec can't encode characters in position 69-70: ordinal not in range(256)，加入charset="utf8"
    # db = pymysql.connect(host='localhost', user='root', password='root', db='mysql', port=3306, charset="utf8")  # 打开数据库
    print('打开数据库成功')
    # cursor = db.cursor()  # 创建一个游标
    with open('../resource/wordlist.txt', 'a+') as f:
        for key in word_mause:  # word_mause是一个字典，模型：{'comment': ['[ˈkɔment]', 'n. 评论，意见；体现，写照', '四级必备词汇']}
            f.writelines(key + '\n')
            # sql = 'INSERT INTO word(id, fayin, fanyi, music, word_tream) values(%s, %s, %s, %s, %s)'  # 构造sql语句
            # try:
                # cursor.execute(sql,
                #             (key, word_mause[key][0], word_mause[key][1], 'music/' + key + '.mp3', word_mause[key][2]))
                # db.commit()  # 插入数据
            # except Exception as e:
                # db.rollback()  # 如果发生异常，则回滚（什么事情都没有发生）
                # print(e.__str__())
        print('数据插入成功')
        # db.close()  # 关闭数据库，记得一定要记得关闭数据库
        # print('数据库成功关闭')


# def creat_table():  # 创建一个表
#     db = pymysql.connect(host='localhost', user='root', password='root', db='movie', port=3306, charset="utf8")
#     print('打开数据库成功')
#     cursor = db.cursor()
#     sql = 'CREATE TABLE IF NOT EXISTS word (id VARCHAR(255) NOT NULL,fayin VARCHAR(255) NOT NULL,fanyi VARCHAR(255) NOT NULL,music VARCHAR(255) NOT NULL,word_tream VARCHAR(255) NOT NULL, PRIMARY KEY (id))'
#     cursor.execute(sql)
#     print('创建表成功')
#     db.close()


def main():
    # creat_table()  # 创建一个表
    url = 'http://word.iciba.com/'
    html = get_urlhtml(url)  # 得到首页的H5代码
    word_all = get_url(html)  # 得到所有classid可能取值的列表
    print('初始化成功开始爬取')
    for num in word_all:  # word_all为classid所有可能的取值
        url_home = 'http://word.iciba.com/?action=courses&classid=' + str(num)  # 利用字符串拼接起来，得到URL网址
        html = get_urlhtml(url_home)
        mess = BeautifulSoup(html, 'lxml')
        li = mess.select('ul li')  # 解析得到所有的课时，其中li的长度就是课时的数量
        if len(li) <= 2:
            continue
        name = mess.select('.word_h2')  # 得到词书名称
        name = name[0]
        r = re.compile(".*?</div>(.*?)</div>")
        name = re.findall(r, str(name))
        name = name[0]  # 得到词书名称
        print('开始爬取' + name)
        for j in range(1, len(li) + 1):  # 利用课时的数量就是course的取值的特性，得到course的取值
            url = 'http://word.iciba.com/?action=words&class=' + str(num) + '&course=' + str(j)  # 得到单词所在的URL网站
            reponse = get_urlhtml(url)
            # print('开始爬取音频')
            # paqumusci(reponse)
            # print('音频文件爬取完成')
            print('开始爬取数据')
            word_mause = paqu_wangye(reponse, name)  # 得到数据字典
            print('开始存储数据')
            cucun(word_mause)  # 存储数据


if __name__ == '__main__':
    main()