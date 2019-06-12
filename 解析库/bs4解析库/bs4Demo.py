# -*- coding: utf-8 -*-

"""
beautifulsoup解析库
"""

__author__ = 'katherinelove'

import requests,logging
from bs4 import BeautifulSoup

def get_page(url):
    headers = {"User-Agent": "ozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36ozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36)",
               "Host": "maoyan.com"}
    r=requests.get(url,headers=headers,verify=False)
    if r.status_code==200:
        r.encoding="utf-8"
        return r.text
    return None

def parser_page(content):
    soup=BeautifulSoup(content,"lxml")
    # print(soup.prettify())
    for dds in soup.find_all(name="dd"):
        index=dds.i.string
        image=dds.find(class_="board-img")['data-src']   #get（） tag['']   tag.attrs['']等效
        title=dds.find(class_="name").get_text()      #get_text() 和    tag.string属性等效
        #选择器返回的是列表即使 只有一个元素
        star=dds.select('.star')[0].string.strip()  #css 选择方法---    tag.select（.class值 #id值 tag）  嵌套时 有空格
        time=dds.find(class_='releasetime').string.strip()
        score=dds.find(class_='integer').string+dds.find(class_='fraction').string
        yield {
            'index':index,
            'image':image,
            'title':title,
            'star':star[3:] if len(star)>3 else " ",
            'time':time[5:] if len(time)>5 else " ",
            'score':score
        }


if __name__ == '__main__':
    logging.captureWarnings(True)
    url='https://maoyan.com/board/4?offset=0'
    content=get_page(url)
    for item in parser_page(content):
        print(item)

