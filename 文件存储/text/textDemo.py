# -*- coding: utf-8 -*-

"""
text
快速方便,不方便检索
"""

__author__ = 'katherinelove'

import requests
from urllib.request import urlopen
from pyquery import PyQuery as pq


if __name__ == '__main__':
    url='https://www.zhihu.com/explore'
    html=urlopen(url).read().decode('utf-8')
    # print(html.read().decode('utf-8'))
    # print(html)
    doc=pq(html)
    divs=doc('.explore-tab .feed-item')
    for div in divs.items():
        question=div.find('h2').text().strip()
        author=div.find('.author-link').text().strip()
        answer=pq(div.find('.content').html()).text().strip()
        # print(answer)
        with open('zhihuComents.txt','a',encoding='utf-8') as f:
            f.write('\n'+"="*50+'\n')
            f.write('\n'.join([question,author,answer]))

    print('done')
    # print(divs)






