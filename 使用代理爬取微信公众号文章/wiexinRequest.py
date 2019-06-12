# -*- coding: utf-8 -*-

"""
WeixinRequest类，继承自Request对象
由于我们需要利用队列（Redis中的list）存储请求，
这里请求包括（连接，请求头，请求方式，超时时间）封装在Request对象中
1.每次请求翻页需要代理来实现，还需要need_proxy参数
2.对于某个请求，需要对应的方法来处理它的响应，需要callback参数（回调函数）
3.如果一个请求失败次数过多，不在请求，需要失败次数参数Failed_time参数
父类具有的属性利用super（）去继承
子类的属性必须重新添加
"""

__author__ = 'katherinelove'

from requests import Request
from Python3网络爬虫开发实战_崔庆才.使用代理爬取微信公众号文章.setting import *

class WeixinRequest(Request):
    def __init__(self,url,callback,method='GET',headers=None,need_proxy=False,fail_time=0,timeout=TIMEOUT):
        # super(WeixinRequest,self).__init__(method,url,headers)   #继承父类的顺序不能乱
        Request.__init__(self,method,url,headers)
        self.callback=callback
        self.need_proxy=need_proxy
        self.fail_time=fail_time
        self.timeout=timeout

