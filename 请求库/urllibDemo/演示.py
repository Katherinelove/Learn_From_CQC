# -*- coding: utf-8 -*-

"""
urllib 演示手稿
urllib包共request,parse,error,robotparser 四个模块
"""

__author__ = 'katherinelove'

from urllib import request,parse,error,robotparser

def 高级请求(url):
    if url==None or url=="":
        return
    #data参数必须是字节型，必须将字典编译成utf-8编码
    data=bytes(parse.urlencode({"name":"kate"}),encoding="utf-8")
    response=request.urlopen(url,timeout=10,data=data)
    print("type(req):",type(response))
    print(response.status,response.reason)
    print(response.read())
    print(response.getheaders())
    print(response.getheader("Server"))

def Request高级请求(url):
    if url==None or url=="":
        return
    #data参数必须是字节型，必须将字典编译成utf-8编码
    data=bytes(parse.urlencode({"name":"kate"}),encoding="utf-8")
    headers={"user_agent":"Mozilla/4.0 (Compatible;MSIE 5.5 Windows NT)",
             "host":"httpbin.org"}
    req=request.Request(url,data=data,headers=headers,method="POST")
    response=request.urlopen(req)
    print("type(req):", type(req))
    print(response.status, response.reason)
    print(response.read())
    print(response.getheaders())

def 解析连接(url):
    if url==None or url=="":
        return
    #六参数
    result=parse.urlparse(url,scheme="https")
    print(result)
    print(parse.urlunparse(result))
    data=['http','www.baidu.com','/index.html','user','id=5', 'comment']
    print(parse.urlunparse(data))
    # 5参数
    result2 = parse.urlsplit(url,scheme="http",allow_fragments=False)
    print(result2)


def 连接url(url1,url2):
    result=parse.urljoin(url1,url2)
    print(result)
    #urlencode 构造url参数时
    base_url="http://www.baidu.com?"
    data={"name":"kate"}
    url=base_url+parse.urlencode(data)
    print(url)
if __name__ == '__main__':
    url="http://www.baidu.com"
    url1="http://httpbin.org/post"
    url2="http://www.baidu.com/index.html;user?id=5#comment"
    #高级请求(url)
    #Request高级请求(url1)
    #解析连接(url2)
    连接url(url1,url2)