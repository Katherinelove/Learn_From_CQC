# -*- coding: utf-8 -*-

"""
参数全是选择器
PQ.text（）  获取内部所有文本
PQ.html（）  获取第一个PQ的html（当前面的PQ包含多个）
PQ.attr（）  获取第一个PQ的attr（当前面的PQ包含多个）
当PQ包含多个PQ类型时，PQs.item()获取迭代对象
上面上个还可以动态修改文档 外加remove（），addClass（），removeClass（）
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
    # for dd in dds.items():
    index=dds.find('.board-index').text()        #当Pyquery只有一个PQ元素是，PQ（选择器）与PQ.find（选择器）作用一致
    title=dds.find('.name').text().strip()
    print(index)
    print(title)


def PQs_find():
    url = 'https://maoyan.com/board/4?offset=0'
    html = get_page(url)
    parser(html)

def 动态修改节点(html):
    doc=pq(html)
    print(doc)
    i=doc('.board-index')
    i.remove_class('board-index-1')
    print(i)
    i.add_class('board-index-1')
    print(i)
    #增改属性
    i.attr("class",'love')
    print(i)
    i.attr("sb",'yeyezaici')
    print(i)
    #改变text
    i.text("kate candy")
    print(i)

    #改变内部html
    i.html('<p>loveyou</p>')
    print(i)


 
if __name__ == '__main__':
    html='''   <dd>
                        <i class="board-index board-index-1">1</i>
    <a href="/films/1203" title="霸王别姬" class="image-link" data-act="boarditem-click" data-val="{movieId:1203}">
      <img src="//ms0.meituan.net/mywww/image/loading_2.e3d934bf.png" alt="" class="poster-default" />
      <img data-src="http://p1.meituan.net/movie/20803f59291c47e1e116c11963ce019e68711.jpg@160w_220h_1e_1c" alt="霸王别姬" class="board-img" />
    </a>
    <div class="board-item-main">
      <div class="board-item-content">
              <div class="movie-item-info">
        <p class="name"><a href="/films/1203" title="霸王别姬" data-act="boarditem-click" data-val="{movieId:1203}">霸王别姬</a></p>
        <p class="star">
                主演：张国荣,张丰毅,巩俐
        </p>
<p class="releasetime">上映时间：1993-01-01</p>    </div>
    <div class="movie-item-number score-num">
<p class="score"><i class="integer">9.</i><i class="fraction">6</i></p>        
    </div>

      </div>
    </div>

                </dd>'''
    # PQs_find()
    动态修改节点(html)