# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from pymongo import MongoClient

class BtmoviePipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    '''
    存入mongodb
    '''
    #这个获取Logger名称
    logger=logging.getLogger(__name__)

    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri=mongo_uri
        self.mongo_db=mongo_db


    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.logger.debug('打开mongodb数据库')
        self.client=MongoClient(self.mongo_uri)
        self.db=self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[item.collection].insert(dict(item))
        self.logger.debug('成功插入数据！')
        return item

    def close_spider(self,spider):
        self.logger.debug('关闭mongodb数据库连接')
        self.client.close()