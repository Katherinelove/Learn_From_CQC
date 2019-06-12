# -*- coding: utf-8 -*-

"""
lxml解析html
"""

__author__ = 'katherinelove'

import requests
from lxml import etree

def get_page(url):
    headers = {"User-Agent": "Mozilla/4.0 (Compatible;MSIE 5.5 Windows NT)",
               "Host": "maoyan.com"}
    r=requests.get(url,headers=headers)
    if r.status_code==200:
        r.encoding="utf-8"
        return r.text
    return None

def parse_page(html):
    index=html.xpath('//i[contains(@class,"board-index")]/text()')
    image=html.xpath('//img/@data-src')
    title=html.xpath('//p[@class="name"]/a/text()')
    star=html.xpath('//p[@class="star"]/text()')
    time=html.xpath('//p[@class="releasetime"]/text()')
    score_integer=html.xpath('//p[@class="score"]/i[@class="integer"]/text()')
    score_fraction=html.xpath('//p[@class="score"]/i[@class="fraction"]/text()')
    for i in range(len(index)):
        yield {
            "index":index[i],
            "image":image[i],
            "title":title[i].strip(),
            "star":star[i].strip()[3:] if len(star[i])>3 else "",
            "time":time[i].strip()[5:] if len(time[i])>5 else "",
            "score":(score_integer[i]+score_fraction[i])
        }
if __name__ == '__main__':
    url="https://maoyan.com/board/4?offset=0"
    text=get_page(url)
    #可以从文件中读取html解析对象
    #html=etree.parse(src,etree.HTMLParser())
    html=etree.HTML(text)      #直接从文本读取解析对象
    # print(etree.tostring(html).decode("utf-8"))   #解析对象转字符串，必须解码为utf-8
    items=parse_page(html)
    for item in items:
        print(item)