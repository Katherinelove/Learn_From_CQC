# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#特别注意这里每一个Pipeline是有优先权限的，否则无效（默认一样），在settings中设置priority的值，越小则优先
#或者在setting中注释掉某个Pipeline这个Pipeline则不生效

import pymongo
from scrapy.exceptions import DropItem

#筛选数据--限制文本长度
class TextPipeline(object):
    def __init__(self):
        self.limit=50    #设置文本长度

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text'])>self.limit:
                item['text']=item['text'][0:self.limit].rstrip()+"..."
                return item               #返回item  数据结构
        else:
            return DropItem('miss text')    #只有两种可能

#将数据存入数据库中  最重要的是重写 def process_item（self，item,spider）方法
class MongoPipeline(object):
    #从类属性中获取---这里框架自动加载
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri=mongo_uri
        self.mongo_db=mongo_db

    #通过设置获取配置
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    #数据库操作
    def open_spider(self,spider):
        #开启spider  连接数据库，并初始化
        self.client=pymongo.MongoClient(host=self.mongo_uri)
        self.db=self.client[self.mongo_db]

    def process_item(self,item,spider):
        #核心操作，插入数据
        #获取item名称作为collection（即表名）
        name=item.__class__.__name__
        self.db[name].insert(dict(item))
        return item            #这里必须返回 item？  可能是为了显示器显示
    def close_spider(self,spider):
        self.client.close()
