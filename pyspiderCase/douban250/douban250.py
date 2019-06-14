#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-06-12 16:33:17
# Project: douBan250

from pyspider.libs.base_handler import *
from pymongo import MongoClient
import re


# 向mongodb中插入数据的类
class MongoWriter(object):

    def __init__(self):
        # 构造对象
        self.client = MongoClient()
        # 获取数据库
        self.db = self.client.douban250
        # 获取集合(表)
        self.collection = self.db.movieIfo

    def insert_result(self, result):
        if result:
            # 向mongodb中插入数据
            self.collection.insert(result)

    def __del__(self):
        # 关闭数据库连接
        self.client.close()


class Handler(BaseHandler):
    # 构造对象
    mongo = MongoWriter()

    crawl_config = {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://movie.douban.com/top250', callback=self.index_page, validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response, fetch_type='js'):
        for item in response.doc('.grid_view > li').items():
            self.crawl(item.find('.info .hd a').attr.href, callback=self.detail_page, validate_cert=False)
        next = response.doc('.next > a').attr.href
        self.crawl(next, callback=self.index_page, validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "moive_name": response.doc('h1 > span').text(),
            "director": response.doc('.attrs > a').text(),
            'actor': response.doc('.actor span').text(),
            'allContent': response.doc('#info').text(),
            'Language': response.doc('#info').text().split('语言:', 1)[1].split('上映日期:', 1)[0].strip(),
            '类型': re.search('类型:(.*?)制片国家/地区', response.doc('#info').text(), re.S).group(1).strip(),
            '制片国家/地区': re.search('制片国家/地区:(.*?)语言', response.doc('#info').text(), re.S).group(1).strip(),
            '上映日期': re.search('上映日期:(.*?)片长', response.doc('#info').text(), re.S).group(1).strip(),
            '片长': re.search('片长:(.*?)又名', response.doc('#info').text(), re.S).group(1).strip(),
            '又名': re.search('又名:(.*?)IMDb链接', response.doc('#info').text(), re.S).group(1).strip(),
            'score': response.doc('.rating_num').text(),
            '评价总数': response.doc('.rating_sum span').text(),
        }

    def on_result(self, result):
        # 执行插入数据的操作
        self.mongo.insert_result(result)
        # 调用原有的数据存储
        super(Handler, self).on_result(result)
