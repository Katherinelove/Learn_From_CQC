# -*- coding: utf-8 -*-

"""
模拟登陆github
并爬取动态信息
session自动获取cookies
表单数据自己构造，post方法请求
"""

__author__ = 'katherinelove'

import requests
from lxml import etree
from pyquery import PyQuery as pq


EMAIL='15281857366@163.com'
PASSWORD='zl.201314shuai'
class Loginer(object):
    def __init__(self):
        self.login_url='https://github.com/login'
        # self.github='https://github.com/'
        self.post_url='https://github.com/session'  #登录成功自动重定向
        self.headers={
            'Host': 'github.com',
            'Referer':'https: // github.com /',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        self.profile_url='https://github.com/settings/profile'
        self.session=requests.Session()

    def token(self):
        '''
        登陆界面，获取证书参数
        :return: authenticity_token
        '''
        response=self.session.get(self.login_url,headers=self.headers)
        if response.status_code==200:
            doc=pq(response.text)
            authenticity_token=doc('#login form input:nth-child(2)').attr('value')
            print(authenticity_token)
            return authenticity_token
        return None

    def login(self):
        '''
        模拟登陆，需要的参数，表单信息
        :return:
        '''
        post_data={
            'commit':'Sign in',
            'utf8': '✓',
            'authenticity_token':self.token(),
            'login:':EMAIL,
            'password':PASSWORD
        }
        response=self.session.post(self.post_url,data=post_data,headers=self.headers)
        if response.status_code==200:
            print('login 成功')    #登录成功自动重定向
        # response=self.session.get(url=self.github,headers=self.headers)
        # if response.status_code==200:
            self.parser_dynamics(response.text)
        else:
            print('访问url：{}失败'.format(self.github))
        # response=self.session.get(self.profile_url,headers=self.headers)
        # if response.status_code==200:
        #     self.parser_profile(response.text)
        # else:
        #     print('访问url：{}失败'.format(self.profile_url))

    def parser_dynamics(self,html):
        '''
        解析动态
        :param html:
        :return: json
        '''
        #由于这一块内容是动态加载，无法直接提取
        selector=etree.HTML(html)
        dynamics=selector.xpath('//div[contains(@class,"news")]//div[position()=3]/div')
        print(dynamics)
        # for item in dynamics:
        #     print(item)
            # dynamic=' '.join(item.xpath('.//div[contains(@class,"d-flex")]/text()'))
            # print(dynamic)


    def parser_profile(self,html):
        doc=pq(html)
        name=doc('#user_profile_name').text()
        print(name)


if __name__ == '__main__':
    loger=Loginer()
    loger.login()
    print('yes')