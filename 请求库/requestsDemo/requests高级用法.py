# -*- coding: utf-8 -*-

"""
进阶
"""

__author__ = 'katherinelove'

import requests


def 文件上传():
    files={"file":open("githb.ico","rb")}   #json格式
    r=requests.post("http://httpbin.org/post",files=files)
    print(r.text)


def cookies获取(url):
    r=requests.get(url)
    print(r.cookies)
    for k,v in r.cookies.items():
        print(k+"="+v)

def 利用cookies维持登录状态(url):
    # cookies=r'_zap=744c2974-e7de-4398-8429-605848618188; ' \
    #         r'd_c0="AFDmOwFMCw6PTsxQTzoFlAsvVL6yzQz5M_4=|1534056290"; ' \
    #         r'_xsrf=UWpm8WCeTSIg7G3PQZIdpHzdpjsxvwXF; ' \
    #         r'capsion_ticket="2|1:0|10:1538048690|14:capsion_ticket|44:NTQwNzZmYjMyMGVmNDNiZDk4YTlmZDMyYmY2NzBkMDI=|c233c5cd22a2ab052a6c1ff0ddf6b242d5eea613f71da7ab99e683ae79b707e5"; ' \
    #         r'z_c0="2|1:0|10:1538048704|4:z_c0|92:Mi4xazdpcEFBQUFBQUFBVU9ZN0FVd0xEaVlBQUFCZ0FsVk53QkNhWEFDN09zYkxwQ25VbTdBalhIaEpYa3lWcmxVbjdB|59cd4530791e855df648eaa0e858f4663fb165824c69700a007383f95d955021";' \
    #         r' q_c1=41cd275ebe9c4e54b6326857968f124e|1538048704000|1538048704000; ' \
    #         r'tst=r;' \
    #         r' tgw_l7_route=53d8274aa4a304c1aeff9b999b2aaa0a'

    headers = {"user_agent": "Mozilla/4.0 (Compatible;MSIE 5.5 Windows NT)",
               "cookie":'BAIDUID=846590C4ECD532A17FFCD378FBA44C3A:FG=1; BIDUPSID=846590C4ECD532A17FFCD378FBA44C3A; PSTM=1533125419; BD_UPN=12314353; ispeed_lsm=2; delPer=0; BD_CK_SAM=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=3; H_PS_PSSID=26522_1422_21096_26350_20929; H_PS_645EC=4fa5%2F7bKFUTSV326V8cBHZzeHplLRCk%2Fb8qZazjc2%2FZyZ9B7Twc57r07DzU; BDUSS=GFKNkVYQjkzU2VpcGh3eTFoT2ludHlSaVF5aDFhR1dkWm9uc3ZLblN6OUROZTViQVFBQUFBJCQAAAAAAAAAAAEAAACtdHMhxM-5rMep1LwyMjIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEOoxltDqMZbV; BD_HOME=1;',
               "host": "www.baidu.com"}
    r=requests.get(url,headers=headers)
    print(r.status_code)
    print(r.text)

def 会话维持():
    requests.get("http://httpbin.org/cookies/set/number/123456789")
    r=requests.get("http://httpbin.org/cookies")
    print("两次cookies不一样",r.text)

    #使用Session对象
    s=requests.Session()
    s.get("http://httpbin.org/cookies/set/number/123456789")
    r=s.get("http://httpbin.org/cookies")
    print("两页面cookies一样：", r.text)

if __name__ == '__main__':
    url="http://www.baidu.com"
    url2="https://www.zhihu.com"
    # 文件上传()
    # cookies获取(url)
    #先登录知乎copy登录后的cookies
    # 利用cookies维持登录状态(url)
    会话维持()   #当post（）请求后，再用get（）请求后面网页相当于打开两个不同的浏览器，使用相同cookie，太繁琐

