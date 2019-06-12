# -*- coding: utf-8 -*-
import scrapy,json
from urllib.parse import urlencode

from images360.items import ImagesItem


class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['image.so.com']
    start_urls = ['http://image.so.com/']

    def start_requests(self):
        #设置初始请求，构造请求参数
        data={}
        base_url='http://image.so.com/zj?'
        #如何动态为字典添加元素
        for page in range(1,self.settings.get('MAX_PAGE')+1):
            data={
                'ch': 'photography',
                'sn': page*30,
                'listtype': 'new'
            }
            params=urlencode(data)
            url=base_url+params
            # print(url)
            yield scrapy.Request(url=url,callback=self.parse)



    def parse(self, response):
        #将字符串反序列化
        # print(response.text)
        result=json.loads(response.text)
        for image in result.get('list'):
            item=ImagesItem()
            item['id']=image.get('imageid')
            item['url']=image.get('qhimg_url')
            item['title']=image.get('group_title')
            item['thumb']=image.get('qhimg_thumb_url')
            yield item