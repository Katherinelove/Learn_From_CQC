# -*- coding: utf-8 -*-

"""
爬取淘宝商品信息
利用selenium+pyquery
"""

__author__ = 'katherinelove'


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
from pymongo import MongoClient
import traceback

class spider(object):
    def __init__(self,keyword='ipad'):
        self.browser=webdriver.Chrome()
        self.wait=WebDriverWait(self.browser,10)
        self.keyword=keyword
    def index_page(self,page):
        '''
        获取当前页页面源代码
        :param page: 页数
        :return: no
        '''
        print('正在爬去第',page,'页')
        try:
            url='https://s.taobao.com/search?q='+quote(self.keyword)
            self.browser.get(url)
            print(self.browser.page_source)
            #浏览器已经加载第一页
            if page>1:#若是访问第二页及以后，加以判断
                input=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form input')))
                submit=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager div.form span.btn.J_Submit')))
                input.clear()
                input.send_keys(page)
                submit.click()
            #等待页面加载完毕
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager ul.items li.item.active span'),str(page)))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item')))
            #成功加载完页面（所获取的部分）
            self.get_products()

        except Exception as e:
            print('获取第{}页出现问题！'.format(page))
            traceback.print_exc()  #本身就是打印函数
            print('重新开始')
            self.index_page(page)
        finally:
            self.browser.close()

    def get_products(self):
        '''
        解析一页商品
        并保存至mongoDB中
        :return: 无
        '''
        html=self.browser.page_source
        doc=pq(html)
        items=doc('.mainsrp-itemlist .items .item').items()  #直接将pQ对象变成迭代器
        for item in items:
            product={
                'image':item.find('.pic .img').attr('data-src'),
                'price':item.find('.price ').text(),
                'deal':item.find('.deal-cnt').text(),
                'title':item.find('.title').text(),
                'shop':item.find('.shop').text(),
                'location':item.find('.location').text()
                }
            #存到mongoDB
            print(product)
            self.save_to_mongoDB(product)

    def save_to_mongoDB(self,product):
        MONGO_URL='localhost'
        MONGO_DB='spider'
        MONGO_COLLECTION='products'
        try:
            client = MongoClient(host=MONGO_URL)
            db = MongoClient[MONGO_DB]
            if db[MONGO_COLLECTION].insert(product):
                print('存储到MongoDB成功！')
        except Exception:
            print('存储到MongoDB失败！')
            traceback.print_exc()
        finally:
            client.close()

MAX_PAGE=100
if __name__ == '__main__':
    taobao=spider('ipad')
    for i in range(1,MAX_PAGE+1):
        taobao.index_page(i)