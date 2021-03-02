# -*- coding: utf-8 -*-

"""

爬虫实验程序
模拟学校官网登录及“健康打卡”的过程，实现根据设定时间自动打卡的功能。

"""

__license__ = "GPL V3"
__version__ = "0.1"
__status__ = "Experimental"

from bs4 import BeautifulSoup as bs
from datetime import datetime
from copy import deepcopy
import requests
import time
import json
import argparse

parser = argparse.ArgumentParser(description='定时自动打卡程序')
parser.add_argument('--path', type=str, default='config.info', required=False, help='配置文件地址')
parser.add_argument('--header_path', type=str, default='header.json', required=False, help='请求头文件地址,json文件')


class Worker:
    def __init__(self):
        path = parser.parse_args().path
        header_path = parser.parse_args().header_path
        with open(header_path, 'r') as f:
            self.header = json.load(f)
        with open(path, 'r', encoding='utf-8') as f:
            self.info = {line.split(':')[0].strip(): line.strip().split(':')[1].strip() for line in
                         f.read().split('\n')}
        self.cookies = None
        self.st = None

    def __get_cookies(self):
        info = {
            'username': self.info['账号'],
            'password': self.info['密码'],
            'captcha': '6Ld5A8YZAAAAABeuNs6p9ImA-Kb4njotgaXxsKLA',
            'g-recaptcha-response': '03AGdBq27D2jp7W2ncY_413s88qaq0pf119kYk09lCPATwSBmpEOG8gnDQ-ku8ySobaiyLS3iNSyGY8909yT4HOZuvamb_TW7zPC1vQQAmsHrpPvFra38XiA5P7JZAZgEv2bh2UlM-yuLZ3ppMTeTBbrDFdJRclSkUrcWMGNnRxMLk2b1nj32QDM06J5qSq8vbFALDFt-I90zGg2CamwcnDnZELe41IbpnlLGmXuShEeqspQEeGD4rXAM2xRufQXFFUvjbgQcJB3uwLDghbXHkYUhbxiYrhkusex_X_X6kcLJPxLBGqFV-aP989oGQx3qv02Ezz5_tBbIwCCulIgT6wNgFFcrKwDZ7XA1nnwnJyRFglnAjeKnDEHdIbAEqHHOSJyg4kIYwV-vJh_fQi2dooSrvQZZUluNSxnLaCGt94kRIf2KjhDYatOALhLzqWIKQOvwuP0JGeKus'
        }
        new_header = deepcopy(self.header)
        new_header['Host'] = 'my.lzu.edu.cn:8080'
        new_header['Referer'] = 'http://my.lzu.edu.cn/'
        html = requests.get('http://my.lzu.edu.cn:8080/login?service=http://my.lzu.edu.cn', headers=new_header)
        soup = bs(html.text, "lxml")
        for i in soup.find_all('input')[2:]:
            info[i['name']] = i['value']
        init_cookies = html.cookies
        print("===> 初始化成功 <===")
        new_header = deepcopy(self.header)
        new_header['Connection'] = 'keep-alive'
        new_header['Content-Length'] = '673'
        new_header['Content-Type'] = 'application/x-www-form-urlencoded'
        new_header['Host'] = 'my.lzu.edu.cn:8080'
        new_header['Origin'] = 'http://my.lzu.edu.cn:8080'
        new_header['Referer'] = 'http://my.lzu.edu.cn:8080/login?service=http://my.lzu.edu.cn'
        html = requests.post('http://my.lzu.edu.cn:8080/login?service=http://my.lzu.edu.cn', headers=new_header,
                             data=info, cookies=init_cookies)
        self.cookies = dict(dict(init_cookies), **dict(html.history[0].cookies))
        print("===> 登录成功 <===")
        return 1

    def __get_st(self):
        new_header = deepcopy(self.header)
        new_header['Connection'] = 'keep-alive'
        new_header['Content-Length'] = '30'
        new_header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        new_header['Host'] = 'my.lzu.edu.cn'
        new_header['Origin'] = 'http://my.lzu.edu.cn'
        new_header['Referer'] = 'http://my.lzu.edu.cn/more'
        new_header['X-Requested-With'] = 'XMLHttpRequest'
        html = requests.post('http://my.lzu.edu.cn/api/getST', data={'service': 'http://127.0.0.1'}, headers=new_header,
                             cookies=self.cookies)
        self.st = html.json()["data"]
        return 1

    def __submit(self):

        new_header = deepcopy(self.header)
        new_header['Connection'] = 'keep-alive'
        new_header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        new_header['Host'] = 'appservice.lzu.edu.cn'
        new_header['Referer'] = 'http://appservice.lzu.edu.cn/dailyReportAll/'
        new_header['X-Requested-With'] = 'XMLHttpRequest'
        html = requests.get(
            'http://appservice.lzu.edu.cn/dailyReportAll/api/auth/login?st={}&PersonID={}'.format(self.st,
                                                                                                  self.info['卡号']),
            headers=new_header, cookies=self.cookies)
        authorization = html.json()['data']['accessToken']
        print("===> 验证信息获取成功 <===")
        new_header = deepcopy(self.header)
        new_header['Authorization'] = authorization
        new_header['Connection'] = 'keep-alive'
        new_header['Content-Length'] = '19'
        new_header['Content-Type'] = 'application/x-www-form-urlencoded'
        new_header['Host'] = 'appservice.lzu.edu.cn'
        new_header['Origin'] = 'http://appservice.lzu.edu.cn'
        new_header['Referer'] = 'http://appservice.lzu.edu.cn/dailyReportAll/'
        s = requests.session()

        html = s.post('http://appservice.lzu.edu.cn/dailyReportAll/api/encryption/getMD5', headers=new_header,
                      data={'cardId': self.info['卡号']},
                      cookies={'iPlanetDirectoryPro': self.cookies['iPlanetDirectoryPro']})
        md5 = html.json()['data']
        print("===> md5获取成功 <===")
        new_header['Content-Length'] = '56'
        html = s.post('http://appservice.lzu.edu.cn/dailyReportAll/api/grtbMrsb/getInfo', headers=new_header,
                      data={'cardId': self.info['卡号'], 'md5': md5})
        bh = html.json()['data']['list'][0]['bh']
        print("===> bh获取成功 <===")
        new_header['Content-Length'] = '316'
        data = {
            'bh': bh,
            'xykh': self.info['卡号'],
            'twfw': self.info.get('温度范围','0'),
            'sfzx': '1' if self.info.get('是否在校','否') == '是' else '0',
            'sfgl': '1' if self.info.get('是否隔离','否') == '是' else '0',
            'szsf': self.info.get('省',''),
            'szds': self.info.get('市',''),
            'szxq': self.info.get('县',''),
            'sfcg': '1' if self.info.get('是否出国','否') == '是' else '0',
            'cgdd': self.info.get('出国地点',''),
            'gldd': self.info.get('隔离地点',''),
            'jzyy': self.info.get('就诊医院',''),
            'bllb': '0',
            'sfjctr': '1' if self.info.get('是否接触过其他人','否') == '是' else '0',
            'jcrysm': self.info.get('亲密接触人说明','') if self.info.get('是否接触过其他人','否') == '是' else '',
            'xgjcjlsj': self.info.get('相关进出时间',''),
            'xgjcjldd': self.info.get('相关进出经历地点',''),
            'xgjcjlsm': self.info.get('相关进出经历说明',''),
            'zcwd': '0.0',
            'zwwd': '0.0',
            'wswd': '0.0',
            'sbr': self.info['姓名'],
            'sjd': ''}
        html = s.post('http://appservice.lzu.edu.cn/dailyReportAll/api/grtbMrsb/submit', headers=new_header, data=data)
        return True if html.json()['message'] == '成功' else False

    def run(self):
        status = False
        while not status:
            try:
                self.__get_cookies()
                print("===> 登录cookies获取成功 <===")
                self.__get_st()
                print("===> st number获取成功 <===")
                status = self.__submit()
                print("===> 打卡成功 <===")
            except Exception as err:
                print(str(err))
                time.sleep(2)
                continue


worker = Worker()
start_hour = int(worker.info['打卡时间h'])
start_minute = int(worker.info['打卡时间m'])
while True:
    t = datetime.now()
    if t.minute == 30 or t.minute == 0:
        print(t)
    if t.hour == start_hour and t.minute == start_minute:
        print('=============开始打卡=============')
        worker.run()
        print('=============打卡结束=============')
    time.sleep(60)
