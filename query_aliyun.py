# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午3:56
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : query_aliyun.py
# @Software: PyCharm

import time, datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import os
import requests
import json

# 检查active.txt是否存在
if not os.path.exists('resource/active.txt'):
    # 调用系统命令行来创建文件
    os.system(r"touch {}".format('active.txt'))

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


def domainQueryFromAliyun(domains):
    '''
    通过万网查询域名
    :param domains: 需要查询的domain列表
    :return:
    '''

    with open('resource/active.txt', 'a+') as activeFile:
        # 记录当前查询日期
        isotimeformat = '%Y-%m-%d %H:%M:%S'
        current_date = time.strftime(isotimeformat, time.localtime(time.time()))
        activeFile.write(current_date + "\n")


    if len(domains) <= 0:
        return

    # 读取所有需要查询的domain
    lines = domains

    print('拼音数据准备完成，开始查询，需要查询的数量:%s' % len(lines))
    query_idx = 0
    # 记录时间
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('\n\n' + current_time)
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
            query = urlopen(request, timeout=30)
        except Exception as error:
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
                colors.YELLOW + "Very nice! domain: %s is available " % query_domain + colors.ENDC + ", query idx:%s" % query_idx)
            with open('resource/active.txt', 'a+') as activeFile:
                # 将可以注册的domain写入到active.txt中
                activeFile.write(query_domain + "\n")
            # 当一个domain可以注册时，我们验证它相关的其他domain是否被注册了
            # name = domain_name.split(".")[0].strip()
            # list = domainQuertFromUniregistry(name)
            # print(str(len(list)) + '个 domain已注册：' + ','.join(list))

        elif http_code == '200' and query_result == '211':  # domain不可以注册
            print("sory domain: %s is not available" % query_domain + ", query idx:%s" % query_idx)

        elif query_result == '213':  # domain查询超时
            print('domain: %s query timeout' % query_domain + ", query idx:%s" % query_idx)

        else:
            print("that is really bad!" + ", query idx:%s" % query_idx)
            print(http_code)
            print(query_domain)
            print(query_result)

        query_idx += 1

def domainQuertFromUniregistry(domain):
    '''
    根据字符查询 查询已经注册domain
    输入domain的名字，请不要包含后缀，比如'.com'
    :param domain: example: goolor
    :return: 已经注册的后缀list
    '''

    headers = {'Host': 'uniregistry.com',
               'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
               'Accept': '*/*',
               'Cookie': 'SRV=web05|W6HqX|W6HkA; locale=zh; session=3ce724d2018118a02af32bd8cb58100ee2009d47gAJVSHNlc3Npb25fZDJjZDZjYzkyMGYzZjNiODgyZmI1ZmEyMjk4MGFhMjc4ZDYwYzdjY2MzY2NiN2U1YzFkM2I5OTE1NDI5ZDQwYnEBLg==',
               'Connection': 'keep-alive',
               'X-CSRF-Token': '62ac4089a0184f566e09bd1e5044152e31e41c20',
               'User-Agent': 'Uniregistry/3.4.5 (com.uniregistry.Uniregistry; build:3253; iOS 12.0.0) Alamofire/4.7.2',

               }

    response = requests.post(url='https://uniregistry.com/api/check/domains', data={'q': domain, 'suggest': 'true'},
                             verify=False, headers=headers)
    res_json = response.content.decode('utf-8')
    '''
    {"suggestions": [{"sld": "goolor", "check": true, "availability": "available", "id": "goolor.link", "tld": "link"}, {"sld": "goolor", "check": false, "availability": "taken", "id": "goolor.com", "tld": "com"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.xyz", "tld": "xyz"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.app", "tld": "app"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.org", "tld": "org"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.help", "tld": "help"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.online", "tld": "online"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.click", "tld": "click"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.photo", "tld": "photo"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.store", "tld": "store"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.life", "tld": "life"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.global", "tld": "global"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.email", "tld": "email"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.tech", "tld": "tech"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.fun", "tld": "fun"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.company", "tld": "company"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.net", "tld": "net"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.info", "tld": "info"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.cloud", "tld": "cloud"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.co", "tld": "co"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.co.uk", "tld": "co.uk"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.services", "tld": "services"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.guru", "tld": "guru"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.club", "tld": "club"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.top", "tld": "top"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.mom", "tld": "mom"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.blog", "tld": "blog"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.biz", "tld": "biz"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.sexy", "tld": "sexy"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.pics", "tld": "pics"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.events", "tld": "events"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.website", "tld": "website"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.site", "tld": "site"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.agency", "tld": "agency"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.group", "tld": "group"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.college", "tld": "college"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.flowers", "tld": "flowers"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.diet", "tld": "diet"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.tattoo", "tld": "tattoo"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.property", "tld": "property"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.lol", "tld": "lol"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.christmas", "tld": "christmas"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.guitars", "tld": "guitars"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.gift", "tld": "gift"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.blackfriday", "tld": "blackfriday"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.car", "tld": "car"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.auto", "tld": "auto"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.cars", "tld": "cars"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.today", "tld": "today"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.london", "tld": "london"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.engineer", "tld": "engineer"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.shoes", "tld": "shoes"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.name.pr", "tld": "name.pr"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.clinic", "tld": "clinic"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.radio.fm", "tld": "radio.fm"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.ceo", "tld": "ceo"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.fans", "tld": "fans"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.pizza", "tld": "pizza"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.fr", "tld": "fr"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.org.uk", "tld": "org.uk"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.ventures", "tld": "ventures"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.codes", "tld": "codes"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.report", "tld": "report"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.exchange", "tld": "exchange"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.lgbt", "tld": "lgbt"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.tw", "tld": "tw"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.enterprises", "tld": "enterprises"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.nl", "tld": "nl"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.build", "tld": "build"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.institute", "tld": "institute"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.immo", "tld": "immo"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.party", "tld": "party"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.game.tw", "tld": "game.tw"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.tips", "tld": "tips"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.clothing", "tld": "clothing"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.green", "tld": "green"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.casa", "tld": "casa"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.gmbh", "tld": "gmbh"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.express", "tld": "express"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.team", "tld": "team"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.camera", "tld": "camera"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.tools", "tld": "tools"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.vision", "tld": "vision"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.promo", "tld": "promo"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.pub", "tld": "pub"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.juegos", "tld": "juegos"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.xxx", "tld": "xxx"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.toys", "tld": "toys"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.vet", "tld": "vet"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.holiday", "tld": "holiday"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.haus", "tld": "haus"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.lease", "tld": "lease"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.rocks", "tld": "rocks"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.one", "tld": "one"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.boutique", "tld": "boutique"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.cheap", "tld": "cheap"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.press", "tld": "press"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.fitness", "tld": "fitness"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.care", "tld": "care"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.run", "tld": "run"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.money", "tld": "money"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.wedding", "tld": "wedding"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.vc", "tld": "vc"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.health", "tld": "health"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.design", "tld": "design"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.desi", "tld": "desi"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.cam", "tld": "cam"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.theatre", "tld": "theatre"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.delivery", "tld": "delivery"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.llc", "tld": "llc"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.cafe", "tld": "cafe"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.salon", "tld": "salon"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.management", "tld": "management"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.digital", "tld": "digital"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.computer", "tld": "computer"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.apartments", "tld": "apartments"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.plumbing", "tld": "plumbing"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.film", "tld": "film"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.expert", "tld": "expert"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.partners", "tld": "partners"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.me", "tld": "me"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.zone", "tld": "zone"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.cab", "tld": "cab"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.fund", "tld": "fund"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.glass", "tld": "glass"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.porn", "tld": "porn"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.coach", "tld": "coach"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.dating", "tld": "dating"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.software", "tld": "software"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.theater", "tld": "theater"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.download", "tld": "download"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.loan", "tld": "loan"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.com.pr", "tld": "com.pr"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.hiv", "tld": "hiv"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.club.tw", "tld": "club.tw"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.host", "tld": "host"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.net.pr", "tld": "net.pr"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.deals", "tld": "deals"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.ph", "tld": "ph"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.democrat", "tld": "democrat"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.com.cn", "tld": "com.cn"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.garden", "tld": "garden"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.edu.ky", "tld": "edu.ky"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.pictures", "tld": "pictures"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.gallery", "tld": "gallery"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.tickets", "tld": "tickets"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.com.au", "tld": "com.au"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.tires", "tld": "tires"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.style", "tld": "style"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.org.mx", "tld": "org.mx"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.cash", "tld": "cash"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.com.mx", "tld": "com.mx"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.io", "tld": "io"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.bingo", "tld": "bingo"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.ltd", "tld": "ltd"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.cn", "tld": "cn"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.lawyer", "tld": "lawyer"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.trade", "tld": "trade"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.reviews", "tld": "reviews"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.ink", "tld": "ink"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.eu", "tld": "eu"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.tours", "tld": "tours"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.country", "tld": "country"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.org.cn", "tld": "org.cn"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.protection", "tld": "protection"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.menu", "tld": "menu"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.equipment", "tld": "equipment"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.bio", "tld": "bio"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.marketing", "tld": "marketing"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.support", "tld": "support"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.miami", "tld": "miami"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.golf", "tld": "golf"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.doctor", "tld": "doctor"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.photos", "tld": "photos"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.diamonds", "tld": "diamonds"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.ski", "tld": "ski"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.media", "tld": "media"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.foundation", "tld": "foundation"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.legal", "tld": "legal"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.us", "tld": "us"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.cricket", "tld": "cricket"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.memorial", "tld": "memorial"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.consulting", "tld": "consulting"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.lc", "tld": "lc"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.vegas", "tld": "vegas"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.capital", "tld": "capital"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.webcam", "tld": "webcam"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.yokohama", "tld": "yokohama"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.sex", "tld": "sex"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.photography", "tld": "photography"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.tax", "tld": "tax"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.nagoya", "tld": "nagoya"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.cx", "tld": "cx"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.education", "tld": "education"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.net.in", "tld": "net.in"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.viajes", "tld": "viajes"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.ooo", "tld": "ooo"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.catering", "tld": "catering"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.storage", "tld": "storage"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.recipes", "tld": "recipes"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.tennis", "tld": "tennis"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.mba", "tld": "mba"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.best", "tld": "best"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.archi", "tld": "archi"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.gratis", "tld": "gratis"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.forsale", "tld": "forsale"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.cleaning", "tld": "cleaning"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.pr", "tld": "pr"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.casino", "tld": "casino"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.tv", "tld": "tv"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.plus", "tld": "plus"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.news", "tld": "news"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.dental", "tld": "dental"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.fm", "tld": "fm"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.financial", "tld": "financial"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.moda", "tld": "moda"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.systems", "tld": "systems"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.kitchen", "tld": "kitchen"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.ninja", "tld": "ninja"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.dentist", "tld": "dentist"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.live", "tld": "live"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.guide", "tld": "guide"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.associates", "tld": "associates"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.technology", "tld": "technology"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.adult", "tld": "adult"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.chat", "tld": "chat"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.futbol", "tld": "futbol"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.tienda", "tld": "tienda"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.international", "tld": "international"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.faith", "tld": "faith"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.surgery", "tld": "surgery"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.earth", "tld": "earth"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.cards", "tld": "cards"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.shopping", "tld": "shopping"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.vacations", "tld": "vacations"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.games", "tld": "games"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.discount", "tld": "discount"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.pro.pr", "tld": "pro.pr"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.fit", "tld": "fit"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.coupons", "tld": "coupons"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.studio", "tld": "studio"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.voto", "tld": "voto"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.red", "tld": "red"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.mn", "tld": "mn"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.net.cn", "tld": "net.cn"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.social", "tld": "social"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.hosting", "tld": "hosting"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.schule", "tld": "schule"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.hospital", "tld": "hospital"}, {"sld": "goolor", "check": true, "availability": "available", "id": "goolor.cruises", "tld": "cruises"}], "results": [], "aftermarket_url_prefix": "//domainnamesales.com/track-affiliate"}
    '''
    result_dict = json.loads(res_json)
    results = result_dict['suggestions']
    list = []
    for item in results:
        check = item['check']
        id = item['id']
        if check is False:
            # check==False 已注册
            list.append(id)

    return list
