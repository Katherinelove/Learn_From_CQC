# -*- coding: utf-8 -*-

"""
Ajax技术爬取微博，并保存至MongoDB中
"""

__author__ = 'katherinelove'

import requests
from pymongo import MongoClient
from pyquery import PyQuery as pq
from urllib.parse import urlencode

base_url='https://m.weibo.cn/api/container/getIndex?'

headers={
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'Host':'m.weibo.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
}


def get_page(page):
    params={
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page':page
    }

    url=base_url+urlencode(params)
    # print(url)
    r=requests.get(url,headers=headers)
    try:
        if r.status_code == 200:
            # print('yes')
            return r.json()
    except:
        print('failed')


def parser_page(json):
    for item in json.get('data').get('cards'):
        item=item.get('mblog')
        weibo={}
        try:
            weibo['id']=item.get('id')
            weibo['text']=pq(item.get('text')).text()
            weibo['attitudes']=item.get('attitudes_count')
            weibo['thumbnail_pic']=item.get('thumbnail_pic')
            weibo['reposts_count']=item.get('reposts_count')
            weibo['comments']=item.get('comments_count')
        except Exception as e:
            print('failed',e)
        yield weibo

def store_to_mongoDb(json):
    client=MongoClient(host='localhost',port=27017)
    db=client.spider
    collection=db.weibo
    collection.insert_one(json)
    client.close()


if __name__ == '__main__':
    for page in range(1,11):   #爬取前10页内容
        json=get_page(page)
        results=parser_page(json)
        # print(json)
        for result in results:
            store_to_mongoDb(result)
    print('all done')