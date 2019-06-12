# -*- coding: utf-8 -*-
import scrapy


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/']


    #设置初始请求方法 及其解析方式
    def start_requests(self):
        yield scrapy.Request(url='http://httpbin.org/post', method='POST', callback=self.parse_post)

    #默认get  默认解析
    def parse(self, response):
        pass

    def parse_post(self, response):
        self.logger.info(response.status)

