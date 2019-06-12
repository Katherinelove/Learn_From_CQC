# -*- coding: utf-8 -*-

"""
redis 运用
1.常用操作和字符串操作方法
2.列表操作方法集   l开头，少数r开头
3.集合操作方法集   s开头
4.有序集合方法集   z开头
5.散列操作方法集   h开头
"""

__author__ = 'katherinelove'

from redis import StrictRedis,ConnectionPool


def string():
    redis=StrictRedis(host='localhost',port=6379,password='',db=0)
    # result=redis.set('name','zengshuai')
    # print(result)
    # redis.set('age',25)
    # redis.set('gender','male')
    # redis.set('score',100)

    #通用方法
    print(redis.exists('name'))
    print(redis.type('name'))
    print(redis.keys('a*'))   #a 开头的 键值
    print(redis.randomkey())  #随机取一个键值
    # redis.rename('score','English')  #重命名
    # print(redis.get('English'))
    print(redis.dbsize())  #size
    redis.expire('English',2)   #设置键值过期时间
    print(redis.ttl('English')) #获取键值过期时间

    redis.move('age',1)       #将键移动到其他数据库
    # redis.flushdb()  #清空本数据库
    # redis.flushall() #清空所有数据库

    #字符串操作
    redis.getset('name','kate')
    print(redis.get('name'))

def list():
    #列表方法l开头，少数r开头
    pool=ConnectionPool(host='localhost',port=6379,password="",db=1)
    redis=StrictRedis(connection_pool=pool)

    redis.rpush('lst',1,2,3,4,5)     #右边加列表值
    redis.lpush('lst',0)        #左边加列列表值



if __name__ == '__main__':
    string()
    # list()
