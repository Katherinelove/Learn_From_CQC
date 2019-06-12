# -*- coding: utf-8 -*-

"""
获取代理
使用元类 获取类方法属性，并添加个数属性
"""

__author__ = 'katherinelove'

from pyquery import PyQuery as pq
from Python3网络爬虫开发实战_崔庆才.ProxyPool_myself.util import get_page


class ProxyMetaClass(type):
    def __new__(cls,name,bases,attrs):
        # {'__module__': '__main__',
        # '__init__': < function RedisClient.__init__at 0x0000000002DC2D90 >,
        #  'add': < function RedisClient.addat 0x0000000002DC2E18 >,
        # 'random': < function RedisClient.random at 0x0000000002DC2EA0 >,
        #  'decrease': < function RedisClient.decrease at 0x0000000002DC2F28 >}
        #类字典中，方法名作为key

        count = 0
        attrs['__CrawlFunc__']=[]   #存储以crawl开头的方法，注意属性不要用此开头
        for k,v in attrs.items():
            if 'crawl' in k:
                attrs['__CrawlFunc__'].append(k)
                count+=1
        attrs['__CrawlFuncCount__']=count
        return type.__new__(cls,name,bases,attrs)

class Crawler(object,metaclass=ProxyMetaClass):
    '''
    使用元类，动态加载属性
    '''
    def get_proxies(self,callback):   #为 attrs['__CrawlFunc__']中的一个元素，即单个方法名
        proxies=[]
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理',proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self,page_count=10):
        '''
        默认爬取前四页的代理
        :param page_count:页码
        :return: 代理
        '''
        start_url="http://www.66ip.cn/{}.html"
        urls=[start_url.format(x) for x in range(1,page_count+1)]  #获取前四页的网址
        for url in urls:
            print('爬取:{}'.format(url))
            page=get_page(url)
            if page:
                doc=pq(page)
                trs=doc('.container table tr:gt(0)').items()    #gt、lt是从0开始
                for tr in trs:
                    ip=tr.find('td:nth-child(1)').text()        #nth是从1开始
                    port=tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip,port])

    # def crawl_proxy360(self):
    #     '''
    #     获取360代理   暂时无法访问
    #     http://www.proxy360.cn/Region/China
    #     :return:
    #     '''
    #     pass

    def crawl_xicidaili(self,page_count=10):
        '''
        西刺代理http://www.xicidaili.com/nn/{page}
        :return:
        '''
        base_url='http://www.xicidaili.com/nn/{}'
        urls=[base_url.format(x) for x in range(1,page_count+1)]
        for url in urls:
            print('爬取{}'.format(url))
            page=get_page(url)
            # print(page)
            if page:
                doc=pq(page)
                trs=doc('#ip_list tr:gt(0)').items()
                for tr in trs:
                    ip=tr.find('td:nth-child(2)').text()     #不出东西，获取的不是属性就是文本
                    port=tr.find('td:nth-child(3)').text()
                    # print(ip,port)
                    yield ':'.join([ip,port])

    def crawl_xicidaili(self,page_count=4):
        '''
        快代理
        url=https://www.kuaidaili.com/ops/proxylist/{page}/
        :return:
        '''
        base_url='https://www.kuaidaili.com/ops/proxylist/{}/'
        urls=[base_url.format(x) for x in range(1,page_count+1)]
        for url in urls:
            print('正在爬去{}'.format(url))
            page=get_page(url,verify=False)
            # print(page)
            if page:
                doc=pq(page)
                trs=doc('#freelist .center tr:gt(0)').items()
                for tr in trs:
                    ip=tr.find('td:nth-child(1)').text()
                    port=tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip,port])



# if __name__ == '__main__':
#     crawler=Crawler()
#     # for item in crawler.crawl_daili66():
#     #     print(item)
#     # for item in crawlercrawler.crawl_xicidaili().crawl_xicidaili():
#     #     print(item)
#     for item in crawler.crawl_xicidaili():
#         print(item)