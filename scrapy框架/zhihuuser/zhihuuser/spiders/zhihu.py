# -*- coding: utf-8 -*-
import scrapy,json
from zhihuuser.items import UserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    #起始用户
    start_user='excited-vczh'

    # 动态构建user API
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'

    # 动态构建关注列表接口API
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    #动态构建关注列表接口API
    fans_url='https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    fans_query='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        #用户信息解析
        yield scrapy.Request(url=self.user_url.format(user=self.start_user,include=self.user_query),callback=self.parse_user)
        #获取关注列表，并解析用户
        # yield scrapy.Request(url=self.follows_url.format(user=self.start_user,include=self.follows_query,offset=0,limit=20),callback=self.parse_follows)
        #获取粉丝列表，并解析用户
        # yield scrapy.Request(url=self.fans_url.format(user=self.start_user,include=self.fans_query,offset=0,limit=20),callback=self.parse_fans)

    def parse_user(self, response):
        # print(response.text)
        #返回是json格式的字符串，必须json反序列化
        result=json.loads(response.text)
        item=UserItem()
        #这里添加逻辑判断，只有item的fields字段在字典中，这为field字段赋值
        for field in item.fields:
            if field in result.keys():
                item[field]=result.get(field)
        yield item

        #这里每解析一个user对象，再获取他的关注列表，从而循环爬取
        yield scrapy.Request(url=self.follows_url.format(user=result.get('url_token'),include=self.follows_query,offset=0,limit=20),callback=self.parse_follows)
        yield scrapy.Request(url=self.fans_url.format(user=result.get('url_token'),include=self.parse_fans,offset=0,limit=20),callback=self.parse_fans)

    def parse_follows(self, response):
        results=json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                #返回每个关注列表用户请求--解析用户
                yield scrapy.Request(url=self.user_url.format(user=result.get('url_token'),include=self.user_query),callback=self.parse_user)
        #获取下一页
        if 'paging' in results.keys() and results.get('paging').get('is_end')==False:
            next_page=results.get('paging').get('next')
            yield scrapy.Request(url=next_page,callback=self.parse_follows)

    def parse_fans(self,response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                # 返回每个关注列表用户请求--解析用户
                yield scrapy.Request(url=self.user_url.format(user=result.get('url_token'), include=self.user_query),
                                     callback=self.parse_user)
        # 获取下一页
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            #翻页是递归本函数
            yield scrapy.Request(url=next_page, callback=self.parse_fans)
