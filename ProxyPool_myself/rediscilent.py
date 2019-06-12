# -*- coding: utf-8 -*-
"""
存储模块
利用redis数据库
method：
add()
random()
decrease()
exist()
max()
count()
all()
"""
__author__ = 'katherinelove'

MAX_SCORE=100
MIN_SCORE=0
INITIAL_SCORE=10
REDIS_HOST='localhost'
REDIS_PORT=6379
REDIS_PASSWORD=None
REDIS_DB=2
REDIS_KEY='proxies'

from redis import StrictRedis
from random import choice


class RedisClient():
    def __init__(self):
        self.redisClient=StrictRedis(host=REDIS_HOST,password=REDIS_PASSWORD,port=REDIS_PORT,db=REDIS_DB,decode_responses=True)
        #decode_responses取出自动解码

    def add(self,proxy,score=INITIAL_SCORE):#利用有序集合   zadd(key,score)
        '''
        添加代理，设置初始分数
        :param proxy: 代理
        :param score: 分数
        :return:
        '''
        if not self.redisClient.zscore(REDIS_KEY,proxy):
            self.redisClient.zadd(REDIS_KEY,score,proxy)
    def random(self):
        '''
        （优先100分,如果不存在则按照分数高低获取
        :return:随机代理
        '''
        result=self.redisClient.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)
        if len(result):
            return choice(result)
        else:   #不存在100分
            result=self.redisClient.zrevrange(REDIS_KEY,0,100)    #返回前100名
            if len(result):
                return result
            else:
                print('代理池中没有代理可用')

    def decrease(self,proxy):
        '''
        每监测一个代理无效，分数-1，如果代理分数小于最小值，则删除代理
        :return:
        '''
        score=self.redisClient.zscore(REDIS_KEY,proxy)
        if score and score>MIN_SCORE:
            print('代理{}当前分数{}减一1'.format(proxy,score))
            return self.redisClient.zincrby(REDIS_KEY,proxy,-1)
        else:
            print('代理{}当前分数{}移除'.format(proxy,score))

    def exist(self,proxy):
        '''
        判断代理是否在集合中
        :param proxy:
        :return: Bool
        '''
        #通过是否可以获取其映射分数监测
        return not self.redisClient.zscore(REDIS_KEY,proxy)==None

    def max(self,proxy):
        '''
        将有效代理置为最高分
        :return:
        '''
        print("代理{}可用，设置为{}".format(proxy,MAX_SCORE))
        self.redisClient.zadd(REDIS_KEY,MAX_SCORE,proxy)
        
    def count(self):
        '''
        获取数量
        :return:
        '''
        return self.redisClient.zcard(REDIS_KEY)

    def all(self):
        '''
        获取全部代理
        :return:
        '''
        return self.redisClient.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)

# if __name__ == '__main__':
#     redisClient=RedisClient()
#     redisClient.add('127.0.0.1')
#     redisClient.add('152.46.27.1')
#     redisClient.add('153.48.27.1')
#     result=redisClient.random()
#     print(result)
#     # redisClient.decrease('127.0.0.1')
#     redisClient.max('127.0.0.1')
#     print(redisClient.count())
#     print(redisClient.all())
#     print(RedisClient.__dict__)