# -*- coding: utf-8 -*-

"""
使用代理爬虫
"""

__author__ = 'katherinelove'

import requests
from get_proxy import get_proxy

PROXY_POOL_URL='http://localhost:5555/random'

if __name__ == '__main__':
    proxy=get_proxy(PROXY_POOL_URL)
    print(proxy)
    proxies={
        'http':'http://'+proxy,
        'https':'https://'+proxy
    }

    try:
        r=requests.get('http://httpbin.org/get',proxies=proxies)
        if r.status_code==200:
            print(r.text)
    except Exception as e:
        print('error:',e.args)