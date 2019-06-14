# -*- coding: utf-8 -*-

"""
编写数据库脚本(放入/usr/lib/python2.7/site-packages/pyspider/database/mysql/下)
"""

__author__ = 'ReaShy'

from six import itervalues
import pymysql


class SQL():
    #数据库初始化
    def __init__(self,database,tablename):
        #数据库连接相关信息
        self.host  = 'localhost'
        self.username = 'root'
        self.password = '123456'
        self.port=3306
        self.charsets = 'utf8'
        self.database = database
        self.tablename=tablename

        #连接对象开关
        self.connection = False
        try:
            self.conn = pymysql.connect(host=self.host,user=self.username,password =self.password,port=self.port,database = self.database)
            self.cursor = self.conn.cursor()
            print("Connect To Mysql!")
            #连接成功打开开关
            self.connection = True
        except:
            print("Cannot Connect To Mysql!")

    #scape函数的作用是给变量加‘’
    #比如你创建的table或者column里有空白字符时
    #错误的查询：select column name1 from hello world tb
    #正确的查询：select `column name1` from `hello world tb`
    def escape(self,string):
        return '%s' % string


    #插入数据到数据库
    def insert(self,values):
        if self.connection:
            tablename = self.escape(self.tablename)
            if values:
                _keys = ",".join(self.escape(k) for k in values)
                _values = ",".join(['%s']*len(values))
                sql_query = 'INSERT INTO {tablename} ({keys}) VALUES ({values})'.format(tablename=tablename, keys=_keys, values=_values)
                # sql_query = "insert into {tablename}({keys}) values ({values})".format(tablename=tablename,keys=_keys,values=_values)
            else:
                sql_query = "replace into {tablename} default values" .format(tablename=tablename)

            try:
                if values:
                    self.cursor.execute(sql_query,tuple(values.values()))
                else:
                    self.cursor.execute(sql_query)
                self.conn.commit()
                print('Insert successfully!')
                return True
            except Exception as e:
                print('insert failed!')
                print( "An Error Occured: ",e.args)
                return False
if __name__=="__main__":
    # conn=pymysql.connect(host='localhost',user='root',password='123456',port=3306,db='spider')
    # cur=conn.cursor()
    # cur.execute('select version()')
    # data=cur.fetchone()
    # print('yes',data)
    mysql=SQL('spider','zengshuai')
    data={'name':'zengshuai','age':20,'sex':'male'}
    # mysql.insert(data)
    print(mysql.insert(data))