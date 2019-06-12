# -*- coding: utf-8 -*-

"""
验证码识别
1.0纯字母数字识别
"""

__author__ = 'katherinelove'

import tesserocr
from PIL import Image

if __name__ == '__main__':
    img=Image.open('D:\GoogleDown\Code.jpg')
    # img.show()
    # text=tesserocr.image_to_text(img)
    # 直接识别效果太差   灰度-二值化
    img=img.convert('L')
    # img.convert('1')
    # img.show()

    threshold=127  #阈值
    table=[]
    for i in range(256):
        if i<threshold:
            table.append(0)
        else:
            table.append(1)
    img=img.point(table,'1')
    img.show()
    text = tesserocr.image_to_text(img)
    print(text)
