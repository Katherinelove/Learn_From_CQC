# -*- coding: utf-8 -*-

"""
csv 用法
delimiter=" ",  设置分隔符
ialect='unix    将空行删除
"""

__author__ = 'katherinelove'

import csv,pandas



if __name__ == '__main__':
    #写入
    with open("csvDemo.csv","w",encoding="utf-8") as csvfile:
        writer=csv.writer(csvfile,delimiter=" ",dialect='unix')
        #print(type(writer))
        writer.writerow(['name','gender','age'])
        writer.writerow(['kare','female','25'])
        writer.writerow(['zengshuai','male','25'])
        writer.writerows([['kare','female','25'],['zengshuai','male','25']])

    #读取
    with open("csvDemo.csv","r",encoding="utf-8") as csvfile:
        reader=csv.reader(csvfile)
        # print(type(reader))
        for line in reader:
            print(line)


    #爬取数据结构化数据  --字典写入
    with open('csvDemo2.csv','w',encoding='utf-8') as f:
        fieldnames=['id','name','age']
        writer=csv.DictWriter(f,fieldnames=fieldnames,dialect="unix")
        writer.writeheader()
        writer.writerow({'id':'1','name':'kate','age':'25'})
        writer.writerow({'id':'2','name':'love','age':'18'})
        writer.writerow({'id':'3','name':'mongo','age':'24'})

    #可以利用pandas 一次读取
    df=pandas.read_csv('csvDemo2.csv')
    print(df)