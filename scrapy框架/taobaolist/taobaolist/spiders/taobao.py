# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request,Spider
from urllib.parse import quote

from taobaolist.items import TaobaolistItem


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com']
    start_urls = ['http://taobao.com/']
    base_url='https://s.taobao.com/search?q='
    cookies={
        't':'8917e8c488fe3181b1d1a22af4b79fac',
        'thw':'cn',
        'v':'0',
        'cna':'6AtgFFg83iMCAd+ACY/KUQxm',
        'cookie2':'5aa01e113d9409e9450495c1aed6f157',
        '_tb_token_':'3eed6fe6d04a9',
        'skt':'b03d2b3369ecad78',
        'csg':'46c46448',
        'uc3':'vt3=F8dByR%2FJyU3S4vT9r7M%3D&id2=UoYcB%2B094OVsLQ%3D%3D&nk2=paC8mmpQj%2Bg%3D&lg2=UtASsssmOIJ0bQ%3D%3D',
        'existShop':'MTU0MTc2MDYwNQ%3D%3D',
        'tracknick':'%5Cu67D2%5Cu6708%5Cu7D2B%5Cu96EA',
        'lgc':'%5Cu67D2%5Cu6708%5Cu7D2B%5Cu96EA',
        '_cc_':'URm48syIZQ%3D%3D',
        'dnk':'%5Cu67D2%5Cu6708%5Cu7D2B%5Cu96EA',
        'tg':'0',
        'enc':'UHzXJ3%2FsvxaOhr2OpuPzVYDI91BfJmNtlq%2FM7iEvAOz9El3s4LsiJyHPXZO7Ks1Hrnhhwd8AIu3fYmTE%2BEJh%2BQ%3D%3D',
        'hng':'CN%7Czh-CN%7CCNY%7C156',
        'mt':'ci=5_1',
        'swfstore':'30453',
        'x':'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0',
        'uc1':'cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&cookie21=WqG3DMC9Fb5mPLIQo9kR&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&existShop=false&pas=0&cookie14=UoTYN4Yz5JroQg%3D%3D&tag=8&lng=zh_CN',
        'whl':'-1%260%260%261541767445840; JSESSIONID=E9C03940F525FB43F64849EEEAB27687',
        'isg':'BNDQiHSOv7YNUmOyHnDAuwC0oR6OipJilwG2esqh2yv-BXCvcqhFcxN02Y1A1Wy7'
    }
    def start_requests(self):
       for keyword in self.settings.get('KEYWORD'):
           for page in range(1,self.settings.get('MAX_PAGE')+1):
            url=self.base_url+quote(keyword)
            yield Request(url=url,callback=self.parse,meta={'page':page},dont_filter=True,cookies=self.cookies)
            #由于请求的url同时相同的，所以分页码利用meta参数传递

    def parse(self, response):
        products=response.xpath('//div[@id="mainsrp-itemlist"]//div[@class="items"]/div[contains(@class,"item ")]')
        for product in products:
            item=TaobaolistItem()
            item['price']="".join(product.xpath('.//div[contains(@class,"price ")]//text()').extract()).strip()
            item['title']="".join(product.xpath('.//div[contains(@class,"title")]//text()').extract()).strip()
            item['shop']="".join(product.xpath('.//div[contains(@class,"shop")]//text()').extract()).strip()
            item['image']="".join(product.xpath('.//div[@class,"pic"]//img[contains(@class,"img")]/@data-src').extract()).strip()
            item['deal']=product.xpath('.//div[contains(@class,"deal-cnt")]//text()').extract_first()
            item['loca']=product.xpath('.//div[contains(@class,"location")]//text()').extract_first()
            yield item