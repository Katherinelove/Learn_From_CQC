# -*- coding: utf-8 -*-
"""
利用mysql存储爬取数据
"""
__author__ = 'katherinelove'

import pymysql
from Python3网络爬虫开发实战_崔庆才.使用代理爬取微信公众号文章.setting import *

class Mysql(object):
    def __init__(self):
        '''
        mysql初始化
        '''
        self.db=pymysql.connect(host=MYSQL_HOST,user=MYSQL_ROOT,password=MYSQL_PASSWORD,db=MYSQL_DB,port=MYSQL_PORT)
        self.cursor=self.db.cursor()

    def insert(self,data,table=TABLE):
        '''
        插入数据
        :param data:
        :param table:
        :return:
        '''
        keys=','.join(data.keys())
        values=','.join(['%s']*len(data))
        sql='insert into {table} ({keys}) values ({values})'.format(table=table,keys=keys,values=values)
        try:
            self.cursor.execute(sql,tuple(data.values()))
            self.db.commit()
            print('插入数据成功', data)  # 方便调试
        except Exception as e:
            print('insert 失败',e.args)
            self.db.rollback()

