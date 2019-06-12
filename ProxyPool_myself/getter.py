# -*- coding: utf-8 -*-

"""
获取模块
作用通过爬去模块获取proxies
"""

__author__ = 'katherinelove'

from Python3网络爬虫开发实战_崔庆才.ProxyPool_myself.crawler import Crawler
from Python3网络爬虫开发实战_崔庆才.ProxyPool_myself.rediscilent import RedisClient


POOL_UPPER_THRESOLD=1000

class Getter(object):
    def __init__(self):
        self.crawler=Crawler()
        self.redisClient=RedisClient()

    #这里为获取器增加开关，当存储模块中的代理超过阈值这停止获取，低于阈值则继续获取proxies
    def is_over_threshod(self):
        return self.redisClient.count() >= POOL_UPPER_THRESOLD
        #等价一下代码
        # if self.redisClient.count()>=POOL_UPPER_THRESOLD:
        #             return True
        #         else:
        #             return False

    def run(self):
        print('获取器执行')
        if  not self.is_over_threshod():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback=self.crawler.__CrawlFunc__[callback_label]
                proxies=self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redisClient.add(proxy)




# if __name__ == '__main__':
#     get=Getter()
#     get.run()
