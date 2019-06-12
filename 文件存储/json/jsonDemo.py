# -*- coding: utf-8 -*-

"""
json
"""

__author__ = 'katherinelove'

import json


str='''
  [
  {
    "name": "曾帅",
    "gender": "male",
    "birthday": "1993-07-10"
  },
  {
    "name": "kate",
    "gender": "female",
    "birthday": "1996-05-01"
  }
]
'''

data= [{
    'name':'曾帅',
    'gender':'male',
    'birthday':'1993-07-10'
    },
    {
    'name':'kate',
    'gender':'female',
    'birthday':'1996-05-01'
    }]

if __name__ == '__main__':
    #反序列化
    lst=json.loads(str)
    print("=============反序列化================")
    print(type(lst),lst)
    print("===============序列化================")
    #序列化
    print(json.dumps(data,indent=2,ensure_ascii=False))

    #存储+序列化
    print("===============存储+序列化（dumps）================")
    with open("jsonDemo.json",'w',encoding="utf-8") as f:
        f.write(json.dumps(data,indent=2,ensure_ascii=False))

    #读取+反序列
    print("===============读取+反序列化(loads)================")
    with open("jsonDemo.json","r") as f:
        str=f.read()
        tempDate=json.loads(str)
        print(tempDate)
    print("===============存储+序列化（dump）================")
    with open('jsonDemo2.json','w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2)
    print("===============读取+反序列化(load)================")
    with open('jsonDemo2.json', 'r') as f:
        da=json.load(f)
        print(da)