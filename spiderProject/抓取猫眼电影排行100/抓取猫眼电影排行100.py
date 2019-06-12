# -*- coding: utf-8 -*-

"""
主页：http://maoyan.com/board/4
观察     每一页10部电影，offset为偏移量，构造10个url
第一页 http://maoyan.com/board/4?offset=0
第二页 http://maoyan.com/board/4?offset=10
第三页 http://maoyan.com/board/4?offset=20
"""

__author__ = 'katherinelove'

import requests,re,json

def get_one_page(url):
    headers = {"User-Agent": "Mozilla/4.0 (Compatible;MSIE 5.5 Windows NT)",
               "Host": "maoyan.com"}
    r=requests.get(url,headers=headers)
    if r.status_code==200:
        r.encoding="utf-8"
        return r.text
    return None

def paser_one_page(html):
    pattern=re.compile(
        r'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S
    )
    items=re.findall(pattern,html)
    for item in items:
        yield {
            "index":item[0].strip(),
            "image":item[1].strip(),
            "title":item[2].strip(),
            "actor":item[3].strip()[3:] if len(item[3])>3 else " ",
            "time":item[4].strip()[5:] if len(item[4])>5 else " ",
            "score":item[5].strip()+item[6].strip()
        }

def write_to_file(content):
    with open("result.txt","a",encoding="utf-8") as f:
        #print(type(json.dumps(content)))
        f.write(json.dumps(content,ensure_ascii=False)+"\n")


def main(offset):
    url = "http://maoyan.com/board/4?offset="+str(offset)
    html = get_one_page(url)
    # print(html)
    items = paser_one_page(html)
    for item in items:
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(i*10)
    print("All done!")