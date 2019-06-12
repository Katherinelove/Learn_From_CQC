# -*- coding: utf-8 -*-

"""
利用redis列表存储WeixinRequest对象
这里存在对象的序列化与反序列化  利用pickle包
"""

__author__ = 'katherinelove'

from Python3网络爬虫开发实战_崔庆才.使用代理爬取微信公众号文章.setting import *
from Python3网络爬虫开发实战_崔庆才.使用代理爬取微信公众号文章.wiexinRequest import WeixinRequest
from redis import StrictRedis
import pickle

class RedisQueue():
    def __init__(self):
        self.db=StrictRedis(host=REDIS_HOST,password=REDIS_PASSWORD,port=REDIS_PORT,db=REDIS_DB)
    def add(self,request):
        '''
        向队列添加序列化后的ruquest对象
        :param request:
        :return:
        '''
        if request==None:
            return False
        if isinstance(request,WeixinRequest):
            self.db.rpush(REDIS_KEY,pickle.dumps(request))          #这里必须对对象序列化
        return False
    def pop(self):
        '''
        取出下一个Request对象，并反序列化
        :return:
        '''
        if self.db.llen(REDIS_KEY):
            return pickle.loads(self.db.lpop(REDIS_KEY))   #切记反序列化，否则只是个二进制文件(字符串)
        else:
            return False

    def empty(self):
        return self.db.llen(REDIS_KEY)==0

