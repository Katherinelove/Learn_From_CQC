# -*- coding: utf-8 -*-

"""
获取代理池中的代理
"""

__author__ = 'katherinelove'

import requests

PROXY_POOL_URL='http://localhost:5555/random'

def get_proxy(url):
    try:
        r=requests.get(url)
        if r.status_code==200:
            return r.text
    except:
        print('连接{}错误'.format(url))

