# -*- coding: utf-8 -*-

"""
运行程序
"""

__author__ = 'katherinelove'

from Python3网络爬虫开发实战_崔庆才.ProxyPool_myself.schedule import Schedule
import io,sys,logging

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')   #改变python默认编码
logging.captureWarnings(True)    #不显示警告


#在最层检查异常，出现异常继续执行
def main():
    try:
        schedule = Schedule()
        schedule.run()
    except:
        main()


if __name__ == '__main__':
    # main()
    schedule = Schedule()
    schedule.run()