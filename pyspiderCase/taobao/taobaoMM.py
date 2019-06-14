#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-11-14 10:17:08
# Project: tbmm

import os
from random import choice
from pyspider.libs.base_handler import *

PAGE_START=1
PAGE_END=100
DIR_PATH=r'E:/teacher_liao/Python3网络爬虫开发实战_崔庆才/pyspiderCase/images'


class Handler(BaseHandler):
    ua =USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
    crawl_config = {
        "headers": {
            "User-Agent": choice(ua)
        },
    }
    def __init__(self):
        self.base_url = 'https://v.taobao.com/v/content/live?page={page}'
        self.page_num = PAGE_START
        self.total_num = PAGE_END
        self.deal=Deal()



    @every(minutes=24 * 60)
    def on_start(self):
        while self.page_num<=self.total_num:
            self.crawl(self.base_url.format(page=str(self.page_num)), callback=self.index_page,validate_cert=False,fetch_type='js')
            self.page_num+=1

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.anchor-profile-info').items():
            self.crawl(each.attr.href, callback=self.detail_page)
    @config(priority=2)
    def detail_page(self, response):
        nickName=response.doc('.next-row .nick span').text()
        image=response.doc('.next-row .nick img.vflag').attr.src
        fans=response.doc('.next-row .fans').text()
        return {
            "nickName": nickName,
            "image": image,
            "fans":fans,
        }


class Deal(object):
    #初始化--若路径没有以 / 结尾  则添加  /
    #若没有存在此路径则添加此路径
    def __init__(self):
        self.path = DIR_PATH
        if not self.path.endswith('/'):
            self.path = self.path + '/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
    #存储图片--二进制
    def saveImg(self, content, path):
        with open(path,'wb') as f:
            f.write(content)

    #不同类别  单独建文件夹
    def mkDir(self, path):
        #这里的path是另外添加的路径
        path = path.strip()
        dir_path = self.path + path
        exists = os.path.exists(dir_path)
        if not exists:
            os.makedirs(dir_path)
            return dir_path
        else:
            return dir_path


    #相当于记录日子
    def saveBrief(self, content, dir_path, name):
        file_name = dir_path + "/" + name + ".txt"
        with open(file_name,'w+') as f:
            f.write(content.encode('utf-8'))

