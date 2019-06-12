# -*- coding: utf-8 -*-

"""
调度器，将模块组装起来
"""

__author__ = 'katherinelove'

# API配置
API_HOST = '0.0.0.0'
API_PORT = 5555
TEST_CYCLE=20   #获取器执行间隔
GETTER_CYCLE=20 #测试器执行间隔
TESTER_ENABLE=True      #三个模块的开关
GETTER_ENABLE=True
API_ENABLE=True

from multiprocessing import Process
import time
from Python3网络爬虫开发实战_崔庆才.ProxyPool_myself.getter import Getter
from Python3网络爬虫开发实战_崔庆才.ProxyPool_myself.tester import Tester
from Python3网络爬虫开发实战_崔庆才.ProxyPool_myself.api import app

class Schedule(object):
    def schedule_getter(self,cycle=GETTER_CYCLE):    #getter测试函数，一个进程
        '''
        定时获取
        :return:
        '''
        getter=Getter()
        while True:
            print('开始抓取代理！')
            getter.run()
            time.sleep(cycle)

    def schedule_tester(self,cycle=TEST_CYCLE):
        '''
        定时测试代理
        :return:
        '''
        tester=Tester()
        while True:
            print('测试器开始运行！')
            tester.run()
            time.sleep(cycle)

    def schedule_api(self):
        '''
        开启api，网络框架获取
        :return:
        '''
        app.run(API_HOST,API_PORT)

    def run(self):
        '''
        程序的入口
        :return:
        '''
        print('代理池开始运行')

        if GETTER_ENABLE:
            getter_process=Process(target=self.schedule_getter)
            getter_process.start()
        if TESTER_ENABLE:
            tester_process=Process(target=self.schedule_tester)
            tester_process.start()
        if API_ENABLE:
            api_process = Process(target=self.schedule_api)
            api_process.start()

