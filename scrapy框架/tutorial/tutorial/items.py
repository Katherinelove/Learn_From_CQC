# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotesItem(scrapy.Item):
    # define the fields for your item here like
    # name = scrapy.Field()
    # 定义爬取的数据结构  相当于字典
    text=scrapy.Field()
    author=scrapy.Field()
    tags=scrapy.Field()
