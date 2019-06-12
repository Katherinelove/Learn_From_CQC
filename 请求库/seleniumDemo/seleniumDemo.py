# -*- coding: utf-8 -*-

"""
selenium 是一款自动化监测工具
可以模拟网页，可以动态渲染页面
而且还可以解析网页
额 外方法     browser.execute_script('javascript'),
browser.back(),browser.forward(),
browser.switch_to_frame('iframeResult'),
browser.execute_script('window.open()'),browser.switch_to_window(browser.window_handles[i])
browser.get_cookies(),browser.add_cookie(),browser.delete_all_cookies()
"""

__author__ = 'katherinelove'

from selenium import webdriver
from  selenium.webdriver.common.by import By
from  selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

# from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait


from selenium.webdriver import ActionChains

import traceback,time


def main():
    # demo1()
    # demo2()
    # demo3下拉到底()
    解析()



def  解析():
    browser = webdriver.Chrome()
    try:
        browser.get('https://www.zhihu.com/explore')
        browser.implicitly_wait(10)
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        result=browser.find_element_by_class_name('question_link')
        print('result:',result)
        print(result.get_attribute('href'))
        print(result.text)

        print(result.id)
        print(result.size)
        print(result.location)
        print(result.tag_name)

        print(browser.get_cookies())
        print(browser.window_handles)

        browser.execute_script('window.open()')
        browser.switch_to_window(browser.window_handles[1])
        browser.get('https://wwww.baidu.com')
        print(browser.current_url)
        print(browser.page_source)

    except Exception as e:
        print("failed!", e)
        traceback.print_exc()



def demo3下拉到底():
    browser = webdriver.Chrome()
    try:
        browser.get('https://www.zhihu.com/explore')
        browser.implicitly_wait(20)
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(5)
    except Exception as e:
        print("failed!", e)
        traceback.print_exc()
    finally:
        browser.close()

def demo2():
    browser=webdriver.Chrome()
    try:
        browser.get('https://www.taobao.com/')
        lis=browser.find_elements_by_css_selector('.service-bd li')
        print(lis)
    except Exception as e:
        print("failed!",e)
        traceback.print_exc()
    finally:
        browser.close()

def demo1():
    browser = webdriver.Chrome()
    try:
        browser.get('https://www.toutiao.com/')
        # # 隐式等待
        # browser.implicitly_wait(5)
        input = browser.find_element_by_class_name('tt-input__inner')
        input.send_keys('街拍')
        input.send_keys(Keys.ENTER)
        wait=WebDriverWait(browser,10,0.5)
        # wait.until(EC.presence_of_element_located((By.NAME,'keyword')))
        print(browser.current_url)   #因为新页面是新窗口，必须切换才能获取新连接
        print(browser.page_source)
        print(browser.get_cookies())
    except Exception as e:
        print('failed!', e)
        traceback.print_exc()
    finally:
        browser.close()


if __name__ == '__main__':
    main()


