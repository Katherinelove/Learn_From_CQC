# -*- coding: utf-8 -*-

"""
检查代理是否有效
"""
__author__ = 'katherinelove'

from Python3网络爬虫开发实战_崔庆才.ProxyPool_myself.rediscilent import RedisClient
import aiohttp,asyncio,time,traceback


VALID_STATUS_CODES=[200]
TEST_URL='http://wwww.baidu.com'
BATCH_TEST_SIZE=10

class Tester(object):
    def __init__(self):
        self.redisClient=RedisClient()

    async def test_single_proxy(self,proxy):
        '''
        测试单个代理，若可以访问则置位最大值，否则-1
        :param proxy:
        :return:
        '''
        conn=aiohttp.TCPConnector(verify_ssl=False)   #建立TCP连接对象--整数不检查
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy,bytes):
                    proxy=proxy.decode('utf-8')
                real_proxy="http://"+proxy
                async with session.get(TEST_URL,proxy=real_proxy,timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        print('{}代理可用'.format(proxy))
                        self.redisClient.max(proxy)
                    else:
                        print('{}请求响应码不合法'.format(proxy))
                        self.redisClient.decrease(proxy)
            except Exception as e:
                print('代理请求失败',proxy)
                # traceback.print_exc()
                self.redisClient.decrease(proxy)      #其他问题未访问成功，分数-1


    def run(self):
        '''
        测试主函数
        :return:
        '''
        print('测试器开始运行')
        try:
            proxies=self.redisClient.all()  #取出所有代理
            loop=asyncio.get_event_loop()
            for i in range(0,len(proxies),BATCH_TEST_SIZE):#每次取出100的次数
                test_proxies=proxies[i:i+BATCH_TEST_SIZE]
                tasks=[self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误',e.args)
            # traceback.print_exc()



# if __name__ == '__main__':
#     tester=Tester()
#     tester.run()