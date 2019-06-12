# -*- coding: utf-8 -*-

"""
requests包
"""

__author__ = 'katherinelove'

import requests

def get一键请求(url):
    if url==None or url=="":
        return
    data={"name":"kate"}
    headers={"user_agent":"Mozilla/4.0 (Compatible;MSIE 5.5 Windows NT)",
             "host":"httpbin.org"}
    response=requests.get(url,params=data,headers=headers)
    print(response.status_code,response.reason)
    print(response.text)
    #字符串转json
    print(response.json())
    print(response.content.decode("utf-8"))   #二进制解码
    print(response.headers)
    print(response.cookies)
    print(response.url)
    print(response.history)

def 抓取二进制文件(url1):
    r=requests.get(url1)
    #获取的是二进制文件
    print(r.text)
    print(r.content)
    with open("githb.ico","wb") as f:
        f.write(r.content)# 写入二进制

def post一键请求(url2):
    data = {"name": "kate"}
    headers = {"user_agent": "Mozilla/4.0 (Compatible;MSIE 5.5 Windows NT)",
               "host": "httpbin.org"}
    r=requests.post(url2,data=data,headers=headers)
    print(r.status_code, r.reason)
    print(r.text)
    # 字符串转json
    print(r.json())
    print(r.content.decode("utf-8"))  # 二进制解码
    print(r.headers)
    print(r.cookies)
    print(r.url)
    print(r.history)
if __name__ == '__main__':
    url="http://httpbin.org/get"
    url1="https://github.com/favicon.ico"
    url2="http://httpbin.org/post"
    #get一键请求(url)
    # 抓取二进制文件(url1)
    post一键请求(url2)