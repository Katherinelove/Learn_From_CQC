# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from btmovie.items import BtmovieItem


class BttiantangSpider(scrapy.Spider):
    name = 'bttiantang'
    allowed_domains = ['www.bttiantang.la']
    start_urls = ['http://www.bttiantang.la/']

    def start_requests(self):
        base_url='https://www.bttiantang.la/sb/{}.html'
        move_types=['爱情','喜剧','科幻','恐怖','动作','战争']
        urls=[base_url.format(quote(type)) for type in move_types]
        print("urls:",urls)
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        moves=response.xpath('//ul[@id="post_list"]/li')
        for move in moves:
            item=BtmovieItem()
            item['name']=move.xpath('.//div[@class="article"]/h2//text()').extract_first()
            item['nickname']=''.join(move.xpath('.//div[@class="entry_post"]/p[1]//text()').extract()).strip()
            item['source']=response.urljoin(move.xpath('//div[contains(@class,"clear")]/a/@href').extract_first())
            item['director']=''.join(move.xpath('.//div[@class="entry_post"]/p[2]//text()').extract()).strip()
            item['actors']=''.join(move.xpath('.//div[@class="entry_post"]/p[3]//text()').extract()).strip()
            item['type'] = ''.join(move.xpath('.//div[@class="entry_post"]/p[4]//text()').extract()).strip()
            item['image']=move.xpath('.//div[@class="thumbnail-full"]//img/@src').extract_first()
            yield item
        #切记返回的是selector对象，必须通过.extract()或.extract_first()提取内容
        #如果使用extract()返回的是一个列表(<class 'list'> ['/sb/战争/1.html'])，会报错raise TypeError("Cannot mix str and non-str arguments")
        #所以提取连接需要用.extract_first()
        next=response.xpath('//div[contains(@class,"container")]/div[@class="pagination"]/a[@class="next"]/@href').extract_first()
        # print(type(next),next)
        next_url=response.urljoin(next)
        # print(next_url)
        yield scrapy.Request(url=next_url,callback=self.parse)



