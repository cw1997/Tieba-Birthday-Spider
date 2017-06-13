#! /usr/bin/env python
# -*- coding: utf-8 -*-

# spider  爬虫操作工具类
# version 0.1.0
# author:changwei [867597730@qq.com]
# website: https://github.com/cw1997
# data:2017-06-12 23:20:04

# runtime env:windows 7 64bit + python 2.7.10


import sys
reload(sys)
sys.setdefaultencoding('utf8')

from TiebaSpider import *
from TiebaUtil import *

class SpiderUtil(object):
    """docstring for SpiderUtil"""
    forum = {}

    def __init__(self, forum_name):
        super(SpiderUtil, self).__init__()
        self.forum_name = forum_name
        tieba_util = TiebaUtil()
        self.forum = tieba_util.getForum(forum_name=forum_name)

    def getFidByFname(self):
        """通过fname贴吧名字获取fid贴吧id"""
        ret = self.forum['forum']['id']
        return ret

    def getMemberNumByFname(self):
        """通过fname贴吧名字获取贴吧会员数量"""
        ret = self.forum['forum']['member_num']
        return ret

    def getRankNumByFname(self):
        """通过fname贴吧名字获取贴吧会员数量"""
        tieba_spider = TiebaSpider()
        ret = tieba_spider.fetchRankNumByForum(self.forum_name)
        return ret

    @staticmethod
    def formatDetail(detail):
        """整理已经抓取到的用户信息"""
        # print detail
        if detail.has_key('birthday'):
            birthday = {}
            birthday_list = []
            birthday_list = detail['birthday'].replace(' ', '') \
                .replace(u'年', '-') \
                .replace(u'月', '-') \
                .replace(u'日', '') \
                .split('-')
            if len(birthday_list) == 3:
                birthday['year'] = birthday_list[0]
                birthday['month'] = birthday_list[1]
                birthday['day'] = birthday_list[2]
                detail['birthday'] = birthday
        return detail
