# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import QuotesItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes=response.css('.quote')
        for quote in quotes:
            #利用定义好的数据结构
            item=QuotesItem()
            item['text']=quote.css('.text::text').extract_first()
            item['author']=quote.css('.author::text').extract_first()
            item['tags']=quote.css('.tags .tag::text').extract()
            yield item
        #获取下一页
        next=response.css('.pager .next a::attr("href")').extract_first()
        url=response.urljoin(next)
        yield scrapy.Request(url=url,callback=self.parse)