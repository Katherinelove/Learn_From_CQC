# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaolistItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #定义MongoDB的容器名 和item字段
    collection='taobao'
    image=scrapy.Field()
    price=scrapy.Field()
    deal=scrapy.Field()
    title=scrapy.Field()
    shop=scrapy.Field()
    location=scrapy.Field()
