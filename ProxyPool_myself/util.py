# -*- coding: utf-8 -*-
"""
工具栏
"""
__author__ = 'katherinelove'


import requests
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

def get_page(url,verify=True):
    if url==None:
        return None
    response=requests.get(url,headers=headers,verify=verify)
    if response.status_code==200:
        response.encoding='utf-8'
        return response.text
