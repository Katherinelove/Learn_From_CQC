# -*- coding: utf-8 -*-

"""
pyquery 解析库
"""

__author__ = 'katherinelove'

import requests
from pyquery import PyQuery as pq

def get_page(url):
    headers = {"User-Agent": "Mozilla/4.0 (Compatible;MSIE 5.5 Windows NT)",
               "Host": "maoyan.com"}
    r=requests.get(url,headers=headers)
    if r.status_code==200:
        r.encoding="utf-8"
        return r.text
    return None

def parser(html):
    doc = pq(html)
    # print(doc,type(doc))
    dds=doc('dd')
    # print(dd,type(dd))
    for dd in dds.items():
        index=dd.find('.board-index').text()         #当Pyquery只有一个PQ元素是，PQ（选择器）与PQ.find（选择器）作用一致
        image=dd('.board-img').attr('data-src')
        title=dd('.name').text().strip()
        star=dd('.star').text()[3:] if len(dd('.star').text())>3 else ""
        time=dd.find('.releasetime').text()[5:] if len(dd.find('.releasetime').text())>5 else ""
        score=dd.find('.integer').text()+dd('.fraction').text()
        yield {
            'index':index,
            'image':image,
            'title':title,
            'star':star,
            'time':time,
            'score':score
        }


if __name__ == '__main__':
    url='https://maoyan.com/board/4?offset=0'
    html=get_page(url)
    for item in parser(html):
        print(item)

