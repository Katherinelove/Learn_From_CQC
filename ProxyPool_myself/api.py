# -*- coding: utf-8 -*-

"""
如何获取代理，直接连接自己的redis数据库，随机获取，可行效率也高
但是泄露了自己的账号和密码
使用Flask库
"""

__author__ = 'katherinelove'

from flask import Flask,g
from Python3网络爬虫开发实战_崔庆才.ProxyPool_myself.rediscilent import RedisClient


app=Flask(__name__)  #初始化
def get_conn():
    if not hasattr(g,'redis'):
        g.redis=RedisClient()
    return g.redis

@app.route('/')
def index():
    return '<h2>welcome to proxy pool system</h2>'
@app.route('/random')
def get_proxy():
    '''
    随机获取代理
    :return:
    '''
    conn=get_conn()
    return conn.random()
@app.route('/count')
def get_counts():
    '''
    获取代理池总数
    :return:
    '''
    conn=get_conn()
    return str(conn.count())

# if __name__ == '__main__':
#     app.run()