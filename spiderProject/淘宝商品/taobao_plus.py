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


browser=webdriver.Chrome()
wait=WebDriverWait(browser,10)
keyword='ipad'
def index_page(page):
    '''
    获取当前页页面源代码
    :param page: 页数
    :return: no
    '''
    print('正在爬去第',page,'页')
    try:
        url='https://s.taobao.com/search?q='+quote(keyword)
        cookies={
            't':'8917e8c488fe3181b1d1a22af4b79fac',
            'thw':'cn',
            'cna':'6AtgFFg83iMCAd+ACY/KUQxm',
            'uc3':'vt3=F8dByR%2FJyU3S4vT9r7M%3D&id2=UoYcB%2B094OVsLQ%3D%3D&nk2=paC8mmpQj%2Bg%3D&lg2=UtASsssmOIJ0bQ%3D%3D',
            'tracknick':'%5Cu67D2%5Cu6708%5Cu7D2B%5Cu96EA',
            'lgc':'%5Cu67D2%5Cu6708%5Cu7D2B%5Cu96EA',
            '_cc_':'URm48syIZQ%3D%3D',
            'tg':'0',
            'enc':'UHzXJ3%2FsvxaOhr2OpuPzVYDI91BfJmNtlq%2FM7iEvAOz9El3s4LsiJyHPXZO7Ks1Hrnhhwd8AIu3fYmTE%2BEJh%2BQ%3D%3D',
            'hng':'CN%7Czh-CN%7CCNY%7C156',
            'mt':'ci=5_1',
            'x':'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0',
            'v':'0',
            'cookie2':'3f2d631244b7f9b38f15e6b28ed2d479',
            '_tb_token_':'e17e7001ed53e',
            'JSESSIONID':'6EA9C380E92C4DC12A57EC1AEFF28F8E',
            'isg':'BJeXu8T_gAgBQwSHvRUvNhMJJgtNz02MBMxRL-nEoWbNGLda8a9ljng6fvij8EO2',
            'uc1':'cookie14=UoTYN4kOLkhqXA%3D%3D',
            'swfstore':'29355'
        }
        browser.get(url)
        print(browser.get_cookies())
        browser.delete_all_cookies()
        browser.add_cookie(cookies)
        # print(browser.page_source)
        #浏览器已经加载第一页
        if page>1:#若是访问第二页及以后，加以判断
            input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form input')))
            submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager div.form span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        #等待页面加载完毕
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager ul.items li.item.active span'),str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item')))
        #成功加载完页面（所获取的部分）
        get_products()
    except Exception as e:
        print('获取第{}页出现问题！'.format(page))
        traceback.print_exc()  #本身就是打印函数
        print('重新开始')
        index_page(page)
    finally:
        get_products()

def get_products():
    '''
    解析一页商品
    并保存至mongoDB中
    :return: 无
    '''
    html=browser.page_source
    # print(html)
    doc=pq(html)
    print('我的断点1')
    items=doc('.mainsrp-itemlist .items .item').items()  #直接将pQ对象变成迭代器
    for item in items:
        print('1')
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
        save_to_mongoDB(product)

def save_to_mongoDB(product):
    MONGO_URL='localhost'
    MONGO_DB='spider'
    MONGO_COLLECTION='products'
    try:
        client = MongoClient(host=MONGO_URL)
        db = client[MONGO_DB]
        if db[MONGO_COLLECTION].insert(product):
            print('存储到MongoDB成功！')
    except Exception:
        print('存储到MongoDB失败！')
        traceback.print_exc()

MAX_PAGE=5
if __name__ == '__main__':
    for i in range(1,MAX_PAGE+1):
        index_page(1)