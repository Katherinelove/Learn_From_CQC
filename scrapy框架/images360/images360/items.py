# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImagesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #这里设置mongodb和mysql的表名
    collection=table='images'
    id=scrapy.Field()
    url=scrapy.Field()
    title=scrapy.Field()
    thumb=scrapy.Field()

