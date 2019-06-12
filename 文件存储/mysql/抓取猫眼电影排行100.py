# -*- coding: utf-8 -*-

"""
主页：http://maoyan.com/board/4
观察     每一页10部电影，offset为偏移量，构造10个url
第一页 http://maoyan.com/board/4?offset=0
第二页 http://maoyan.com/board/4?offset=10
第三页 http://maoyan.com/board/4?offset=20
"""

__author__ = 'katherinelove'

import requests,re,json,pymysql

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
            "idx":item[0].strip(),
            "image":item[1].strip(),
            "title":item[2].strip(),
            "star":item[3].strip()[3:] if len(item[3])>3 else " ",
            "dtime":item[4].strip()[5:] if len(item[4])>5 else " ",
            "score":item[5].strip()+item[6].strip()
        }

def write_to_file(content):
    with open("result.txt","a",encoding="utf-8") as f:
        #print(type(json.dumps(content)))
        f.write(json.dumps(content,ensure_ascii=False)+"\n")

#单纯插入
def insert(content):
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='spider', port=3306)
    # print(content)
    # print(content.keys())
    # print(content.values())
    # print(len(content))
    # print("connectec")
    cur = conn.cursor()
    sql='INSERT INTO maoyan (idx,image,title,star,dtime,score) values (%s,%s,%s,%s,%s,%s)'
    try:
        cur.execute(sql,tuple(content.values()))
        conn.commit()
    except:
        print('failed!')
        conn.rollback()
    conn.close()

#字典动态插入
def only_insert(content):
    conn=pymysql.connect(host='localhost',user='root',password='123456',db='spider',port=3306)
    # print(content)
    # print(content.keys())
    # print(content.values())
    # print(len(content))
    # print("connectec")
    cur=conn.cursor()
    table='maoyan'
    keys=','.join(content.keys())
    values=','.join(['%s']*len(content))
    sql='insert into {table} ({keys}) values ({values})'.format(table=table,keys=keys,values=values)

    cur.execute(sql,tuple(content.values()))
    conn.commit()
    conn.close()

#插入更新
def write_to_mysql(content):
    #content 为一行记录 字典格式
    #在插入的同时     动态实现更新  主键重复则更新，不存在则插入
    conn=pymysql.connect(host='localhost',user='root',password='123456',db='spider',port=3306)
    cur=conn.cursor()

    table='maoyan'
    # 动态构造 insert into {table} ({keys}) values (%s*len(字典))  on duplicate key  update id=*,name=*,..利用列表生成式构造
    # 传入的参数时一个元祖
    keys=','.join(content.keys())
    values=','.join(['%s']*len(content))
    sql='INSERT INTO {table} ({keys}) values ({values}) on duplicate key  update'.format(table=table,keys=keys,values=values)
    update=','.join([' {key}=%s'.format(key=key) for key in content])
    sql+=update

    try:
        if cur.execute(sql,tuple(content.values())*2):
            conn.commit()
    except:
        conn.rollback()
    conn.close()


def read_from_mysql():
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='spider', port=3306)
    cur = conn.cursor()
    sql='select * from maoyan'

    cur.execute(sql)

    # 取一条数据
    one=cur.fetchone()
    print('one: ',one)

    #取全部数据  数据量大是不可取
    all=cur.fetchall()
    print('all: ',all)

    #数据量大时循环 一个一个取
    cur.execute(sql)
    one=cur.fetchone()
    while one:
        print(one)
        one=cur.fetchone()



def main(offset):
    url = "http://maoyan.com/board/4?offset="+str(offset)
    html = get_one_page(url)
    # print(html)
    items = paser_one_page(html)
    for item in items:
        # write_to_file(item)
        write_to_mysql(item)
        # only_insert(item)
        # insert(item)


if __name__ == '__main__':
    # for i in range(10):
    #     main(i*10)
    # print("All done!")
    read_from_mysql()