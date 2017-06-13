#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Tieba-Spider  贴吧信息爬虫类
# version 0.1.0
# author:changwei [867597730@qq.com]
# website: https://github.com/cw1997
# 2017-06-12 06:05:11


import sys
reload(sys)
sys.setdefaultencoding('utf8')

# import bs4
import requests
from bs4 import BeautifulSoup

from config import *

# from tieba import TiebaUtil

class TiebaSpider(object):
    """贴吧信息爬虫类"""
    html_parser = "html.parser" # or html5lib

    def __init__(self):
        pass
        # super(TiebaSpider, self).__init__()
        # self.arg = arg

    def fetchMembersByForum(self, forum_name, page=1):
        members = []
        url = 'http://tieba.baidu.com/f/like/furank'
        kw = str(forum_name)
        pn = str(page)
        params = {'kw': kw, 'pn': pn, 'ie': 'utf-8'}
        r = requests.get(url, params, timeout=config['timeout'])
        content = r.content
        soup = BeautifulSoup(content, self.html_parser)
        # print soup.prettify()
        members_soup = soup.find_all("a", {"class": ["drl_item_name_top", "drl_item_name_nor"]})
        for m in members_soup:
            members.append(m.get_text())
        return members

    def fetchDetailByUsername(self, username):
        detail = {}
        url = 'https://www.baidu.com/p/%s/detail?ie=utf-8' % username
        try:
            r = requests.get(url, timeout=config['timeout'])
        except Exception, e:
            return detail
        else:
            detail['username'] = username
        finally:
            pass
        content = r.content
        soup = BeautifulSoup(content, self.html_parser)
        # print soup.prettify()
        attr_soup = soup.find_all("span", {"class": "profile-attr"})
        cnt_soup = soup.find_all("span", {"class": "profile-cnt"})
        # 因为cnt_soup比attr_soup少，是所以使用cnt_soup来遍历
        for i in range(len(cnt_soup)):
            attr = attr_soup[i].get_text()
            # print attr
            if attr == u"个人简介":
                detail['introduce'] = cnt = cnt_soup[i].get_text()
            if attr == u"性别":
                detail['gender'] = cnt = cnt_soup[i].get_text()
            if attr == u"出生地":
                detail['homeplace'] = cnt = cnt_soup[i].get_text()
            if attr == u"血型":
                detail['blood_type'] = cnt = cnt_soup[i].get_text()
            if attr == u"生日":
                detail['birthday'] = cnt = cnt_soup[i].get_text()
            if attr == u"居住地":
                detail['address'] = cnt = cnt_soup[i].get_text()
        return detail

    def fetchRankNumByForum(self, forum_name):
        """获取贴吧排行榜用户"""
        url = 'http://tieba.baidu.com/f/like/furank'
        kw = str(forum_name)
        params = {'kw': kw, 'pn': 1, 'ie': 'utf-8'}
        r = requests.get(url, params, timeout=config['timeout'])
        content = r.content
        soup = BeautifulSoup(content, self.html_parser)
        # print soup.prettify()
        num = soup.find('span', {'class': 'drl_info_txt_gray'}).get_text()
        return num
