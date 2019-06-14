#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-06-14 21:22:27
# Project: qunaerDemo

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://travel.qunar.com/travelbook/list.htm', callback=self.index_page,validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.b_strategy_list > li').items():
            self.crawl(each.find('.tit a').attr.href, callback=self.detail_page,validate_cert=False,fetch_type='js')
        next=response.doc('.next').attr.href
        self.crawl(next, callback=self.index_page,validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('.title > a').text(),
            "date": response.doc('.when .data').text(),
            "day": response.doc('.howlong .data').text(),
            "人均费用": response.doc('.howmuch .data').text(),
            "人": response.doc('.who .data').text(),
            "玩法": response.doc('.how .data').text(),
            "文本": response.doc('#b_panel_schedule').text(),
            "images":response.doc('.cover_img').attr.src
        }
