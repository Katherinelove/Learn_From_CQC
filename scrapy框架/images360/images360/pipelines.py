# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging,pymysql,traceback
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem

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

class MysqlPipeline(object):
    '''
    存入mongodb
    '''
    #这个获取Logger名称

    logger=logging.getLogger(__name__)

    def __init__(self,mysql_host,mysql_user,mysql_password,mysql_db,mysql_port):
        self.mysql_host=mysql_host
        self.mysql_user=mysql_user
        self.mysql_password=mysql_password
        self.mysql_db=mysql_db
        self.mysql_port=mysql_port

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_port=crawler.settings.get('MYSQL_PORT'),
            mysql_db=crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self,spider):
        self.logger.debug('打开mysql数据库')
        self.db=pymysql.connect(self.mysql_host,self.mysql_user,self.mysql_password,self.mysql_db,self.mysql_port)
        self.cur=self.db.cursor()

    def process_item(self, item, spider):
        data=dict(item)
        keys=','.join(data.keys())
        values=','.join(['%s']*len(data))
        try:
            sql='insert into {table} ({keys}) values ({values})'.format(table=item.table,keys=keys,values=values)
            self.cur.execute(sql,tuple(data.values()))
            self.db.commit()
            self.logger.debug('成功插入数据！')
        except:
            print('mysql 插入数据失败！')
            traceback.print_exc()
            self.db.rollback()
        return item

    def close_spider(self,spider):
        self.logger.debug('关闭mysql数据库连接')
        self.db.close()

class ImagePipeline(ImagesPipeline):
    '''
    scrapy 提供了专门下载的Pipleline ，下载过程支持异步和多线程，下载十分高效
    继承自ImagesPipeline 并修改部分逻辑
    '''
    def file_path(self, request, response=None, info=None):
        #获取存储的文件名
        url=request.url
        file_name=url.split('/')[-1]
        return file_name

    def get_media_requests(self, item, info):
        yield Request(item['url'])    #返回下载图片的请求对象

    def item_completed(self, results, item, info):
        '''这一步是，下载完成时，筛选成功下载的图片'''
        #results是一个记录的是下载成功或失败的记录  [(),(),(),....,()]
        print(results)
        image_paths=[x['path'] for ok,x in results if ok]
        if not image_paths:
            DropItem('图片下载失败')
        return item
