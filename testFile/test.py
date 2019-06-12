# -*- coding: utf-8 -*-

"""
模块安装监测
"""

__author__ = 'katherinelove'

from selenium import webdriver
import aiohttp,lxml,bs4,pyquery

if __name__ == '__main__':
    #browser=webdriver.Chrome()
    browser=webdriver.PhantomJS()
    browser.get("http://www.baidu.com")
    print(browser.current_url)
