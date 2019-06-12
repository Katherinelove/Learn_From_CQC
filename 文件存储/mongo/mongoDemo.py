# -*- coding: utf-8 -*-

"""
mongo 数据库的使用
"""

__author__ = 'katherinelove'

import pymongo

zengshuai={
    'id':'2017020016',
    'name':'zengshuai',
    'age':25,
    'gender':'male'
}

lianghui={
    'id':'2017020017',
    'name':'lianghui',
    'age':24,
    'gender':'male'
}

zhanglulu={
    'id':'2017020019',
    'name':'zhanglulu',
    'age':23,
    'gender':'female'
}

liuyanyan={
    'id':'2017020019',
    'name':'liuyanyan',
    'age':23,
    'gender':'female'
}



def inset_data():
    conn = pymongo.MongoClient(host="localhost", port=27017)
    print('连接数据库成功')
    db = conn.students  # 指定数据库
    collection = db.dixin  # 指定集合
    collection.insert_one(zengshuai)                  #官方不推荐inser，可使用insert_one() insert_many()
    result=collection.insert_many([lianghui,zhanglulu,liuyanyan])    #[列表]
    print('插入成功')
    print(type(result),result)
    conn.close()


def search():
    client=pymongo.MongoClient(host='localhost',port=27017)
    db=client.students
    collection=db.dixin
    result=collection.find_one({'name':'zengshuai'})
    print(type(result),result)
    results=collection.find({'age':{'$gt':20}})
    print("相当于迭代器",type(results))
    for result in results:
        print(result)

    #计数
    count=collection.find().count()
    print(count)

    #排序
    sort_result=collection.find().sort('name',pymongo.ASCENDING)
    print(type(sort_result))
    print([result['name'] for result in sort_result])

    #skip()
    sort_result = collection.find().sort('name', pymongo.ASCENDING).skip(1)
    print([result['name'] for result in sort_result])

    #limit()
    sort_result = collection.find().sort('name', pymongo.ASCENDING).skip(1).limit(2)
    print([result['name'] for result in sort_result])

    client.close()



def update():
    client=pymongo.MongoClient(host="localhost",port=27017)
    db=client.students
    collection=db.dixin

    condition={'name':'zengshuai'}    #查询条件
    zengshuai=collection.find_one(condition)
    zengshuai['age']=20           #修改值
    #更新
    result=collection.update_one(condition,{'$set':zengshuai})
    print(type(result),result)
    print(result.matched_count,result.modified_count)

    client.close()


def delete():
    client=pymongo.MongoClient(host='localhost',port=27017)
    db=client.students
    collection=db.dixin

    condition={'name':'liuyanyan'}
    result=collection.delete_one(condition)
    print(result)

    client.close()

if __name__ == '__main__':
    # inset_data()
    # search()
    # update()
    delete()