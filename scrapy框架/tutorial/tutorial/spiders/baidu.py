# -*- coding: utf-8 -*-
import scrapy


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    #只更改默认方法  切记这里是return不是yield生成生成器
    def make_requests_from_url(self, url):
        return scrapy.Request(url=url,callback=self.parse_get)

    def parse(self, response):
        pass

    def parse_get(self,response):
        self.logger.info('love you!')
