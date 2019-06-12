# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BtmovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection='bt_movies'
    name=scrapy.Field()
    nickname=scrapy.Field()
    source=scrapy.Field()
    director=scrapy.Field()
    actors=scrapy.Field()
    type=scrapy.Field()
    image=scrapy.Field()
