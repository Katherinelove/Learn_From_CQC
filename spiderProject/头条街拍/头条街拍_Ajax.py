# -*- coding: utf-8 -*-

"""
url=https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D
爬取头条街拍照片
分标题自动创建文件夹
根据图片内容的md5值去重
"""

__author__ = 'katherinelove'

import os,requests
from urllib.parse import urlencode,urljoin
from hashlib import md5
from multiprocessing.pool import Pool

headers={
    'Host': 'www.toutiao.com',
    'Referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
def get_page(offset):
    base_url='https://www.toutiao.com/search_content/?'
    params={
        'offset':offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab'
    }
    url=base_url+urlencode(params)
    # print(url)
    try:
        r = requests.get(url,headers=headers)
        if r.status_code==200:
            # print('成功获取！')
            return r.json()
    except requests.ConnectionError as e:
        print('failed',e)

def get_image(json):
    if json.get('data'):     #添加过滤条件
        for items in json.get('data'):
            try:
                title=items.get('title')
                #url:"//p1.pstatp.com/list/pgc-image/1540012850605332bd56dc5"               小照片连接
                #large_image_url:"http://p1.pstatp.com/large/pgc-image/154001285034382f3bd4db9"  大照片连接  list-large
                images=items.get('image_list')
                for image in images:
                    image_url =urljoin('http:', image.get('url')).replace('list', 'large', 1)
                    # image_url=image.get('url')
                    # print('image:', image_url)
                    yield {
                        'title':title,
                        'image_url':image_url
                    }
            except Exception as e:
                print('get failed',e)

def save_images(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        r=requests.get(item.get('image_url'))
        # print(item.get('image_url'))
        if r.status_code==200:  #访问成功
            file_path="{0}/{1}.{2}".format(item.get('title'),md5(r.content).hexdigest(),'jpg')  #这里直接是路径，不是创建路径
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f :
                    f.write(r.content)
            else:
                print('Already Download',file_path)
    except requests.ConnectionError as e:
        print('Failed to download',e)

def main(offset):
    json=get_page(offset)
    if json==None:
        return None
    for item in get_image(json):  #迭代器
        save_images(item)

#爬取20页内容
GROUP_START=1
GROUP_END=20
if __name__ == '__main__':
    #使用对进程秒爬
    pool=Pool()
    groups=([x*20 for x in range(GROUP_START,GROUP_END+1)])   #参数时Tuple
    pool.map(main,groups)  #添加到进程池中
    pool.close()
    pool.join()
    print('all download!')

