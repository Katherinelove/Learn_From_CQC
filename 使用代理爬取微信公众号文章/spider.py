# -*- coding: utf-8 -*-

"""
调度器，核心代码
"""

__author__ = 'katherinelove'

from Python3网络爬虫开发实战_崔庆才.使用代理爬取微信公众号文章.wiexinRequest import WeixinRequest
from Python3网络爬虫开发实战_崔庆才.使用代理爬取微信公众号文章.db import RedisQueue
from Python3网络爬虫开发实战_崔庆才.使用代理爬取微信公众号文章.setting import *
from Python3网络爬虫开发实战_崔庆才.使用代理爬取微信公众号文章.mysqlDb import Mysql
from urllib.parse import urlencode
from requests import Session
from pyquery import PyQuery as pq
import requests
import sys
sys.setrecursionlimit(1000000)   #解决超过最大递归深度（RecursionError: maximum recursion depth exceeded）

class Spider():
    base_url='https://weixin.sogou.com/weixin'
    keyword='NBA'
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie':'ABTEST=0|1541062039|v1; SUID=8F0980DF2028940A000000005BDABD98; SUID=8F0980DF1F13940A000000005BDABD9A; weixinIndexVisited=1; SUV=006F5960DF80098F5BDABDA0C3D1F729; SNUID=76F07927F9FD816F80D4A11AF947E9F0; ppinf=5|1541062099|1542271699|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo2MzolRTAlQjglODglRTAlQjglQjglRTAlQjklOEElRTAlQjglOUElMjAlNUIlRTYlOUMlQkElRTYlOTklQkElNUR8Y3J0OjEwOjE1NDEwNjIwOTl8cmVmbmljazo2MzolRTAlQjglODglRTAlQjglQjglRTAlQjklOEElRTAlQjglOUElMjAlNUIlRTYlOUMlQkElRTYlOTklQkElNUR8dXNlcmlkOjQ0Om85dDJsdURILWFDLV8yNmpRUmVpVzR5UzB2dEVAd2VpeGluLnNvaHUuY29tfA; pprdig=YUL-UemIz8HW9MgBRVU0IkH2Dqz6nGILQsLxsF_wd3-QMP3pnjwQ8ipquiOa4liXkB-z3Aipt-F1BVd_LKmQsoh6I2k5Fly9mP_0w5peE6qXyeizGJmVppUFaJoM4lUFO6zl6euGpgBqC2kzrkbWZdfLhUlOcqwOeEvRzC0QW2Y; sgid=25-37744551-AVvavdMicSRGqaZXV3GZvGcU; sct=2; JSESSIONID=aaaddBJlNiiA2eOnObaBw; ppmdig=154114171500000097c6f4792e7f0c932ab5c0bc2c5d2c96; IPLOC=CN5101',
        'Host': 'weixin.sogou.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    session=Session()
    queue=RedisQueue()
    mysql=Mysql()

    def start(self):
        '''
        第一步，向队列中加入第一个weixinrequest
        :return:
        '''
        #初始化session的headers---维持对话
        self.session.headers.update(self.headers)
        start_url=self.base_url+"?"+urlencode({'query':self.keyword,'type':2})
        weixin_request=WeixinRequest(url=start_url,callback=self.parser_index,need_proxy=False,fail_time=0)
        self.queue.add(weixin_request)

    def schedule(self):
        '''调度请求'''
        while not self.queue.empty():
            weixin_request=self.queue.pop()
            callback=weixin_request.callback  #这是一个函数地址，相当于改名
            print('正在爬去网址：',weixin_request.url)
            response=self.request(weixin_request)   #第一个响应
            if response and response.status_code in VAILD_STATUS:
                results=list(callback(response))  #获取更多响应列表
                if results:
                    for result in results:
                        print('New result:',result)             #方便调试---重点地方
                        if isinstance(result,WeixinRequest):   #parser_index()获取的请求对象
                            self.queue.add(result)             #parsers_detail()获取的字典，存入数据库
                        if isinstance(result,dict):
                            self.mysql.insert(result)           #存入mysql数据库
                #结果为空这表示访问失败
                else:
                    self.error(weixin_request)
            else:
                self.error(weixin_request)

    def error(self,weixin_request):
        '''
        处理错误，多次访问失败，剔除
        :param weixin_request:
        :return:
        '''
        weixin_request.fail_time+=1
        print('Request failed',weixin_request.fail_time,'times',weixin_request.url)
        if weixin_request.fail_time<MAX_FAIL_TIME:
            self.queue.add(weixin_request)

    def request(self,weixin_request):
        '''
        根据请求对象，请求响应
        :param weixin_request: 请求
        :return: 响应Response对象
        '''
        # weixin_request = self.queue.pop()
        #         # #callback = weixin_request.callback  # 这是一个函数地址，相当于改名
        #         # print('Schedile', weixin_request.url)

        #重点，根据是否需要代理，判断是否使用代理请求
        try:
            # 使用代理
            if weixin_request.need_proxy:
                proxy=self.get_proxy()
                print('using proxy:',proxy)
                if proxy:
                    proxies={
                        'http':'http://'+proxy,
                        'https':'https://'+proxy
                    }
                #注意这里返回的response对象，并非文本
                return self.session.send(weixin_request.prepare(),proxies=proxies,timeout=weixin_request.timeout,verify=False)
            #不使用代理
            return self.session.send(weixin_request.prepare(),timeout=weixin_request.timeout,verify=False)
        # return self.session.get('https://weixin.sogou.com/weixin?query=NBA&type=2')
        except Exception as e:
            print('请求访问网址失败：{}！'.format(weixin_request.url))
            print(e.args)
            return False     #方便判断

    def get_proxy(self,url=PROXY_URL):
        '''
        随机获取代理
        :return: 代理
        '''
        if int(requests.get(PROXY_SIZE).text):
            r=requests.get(url)
            return r.text

    def parser_index(self,response):
        '''
        解析索引页
        :param response: 响应
        :return: 新的响应
        '''

        doc=pq(response.text)
        items=doc('.news-box .news-list li .txt-box h3 a').items()
        for item in items:
            url=item.attr('href')
            weixin_request=WeixinRequest(url=url,callback=self.parser_detail)  #解析具体内容不用代理
            yield weixin_request
        next=doc('#sogou_next').attr('href')
        #巧妙在于，前面循环文章，最后一个返回的是下一页的解析
        if next:#是否有下一页
            next_url=self.base_url+str(next)
            weixin_request=WeixinRequest(url=next_url,callback=self.parser_index,need_proxy=False)   #解析每一页用代理
            yield weixin_request

    def parser_detail(self,resposne):
        '''
        解析详情页
        :param resposne: 响应
        :return:公众号文章dict
        '''
        doc=pq(resposne.text)
        title=doc('#activity-name').text().strip()
        content=doc('#js_content').text().strip()
        date=doc('#post-date').text()
        # wechat=doc('#meta_content span:nth-child(2)').text()
        wechat = doc('#js_profile_qrcode div p:nth-child(3) span').text()
        nickName=doc('#js_profile_qrcode strong.profile_nickname').text()
        yield {
            'title':title,
            'content':content,
            # 'date':date,
            'wechat':wechat,
            'nickName':nickName
        }

    def run(self):
        '''
        入口
        :return:
        '''
        self.start()
        self.schedule()


if __name__ == '__main__':
    schedule=Spider()
    schedule.run()
    # schedule.start()
