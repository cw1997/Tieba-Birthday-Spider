#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Tieba-Util  贴吧操作工具类
# version 0.1.0
# author:changwei [867597730@qq.com]
# website: https://github.com/cw1997
# 2017-06-12 04:25:16

import urllib2
import json
import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class TiebaUtil(object):
    """贴吧操作工具类"""
    bduss = ''

    def __init__(self):
        pass
        # super(ClassName, self).__init__()
        # login(bduss)

    def login(self, bduss):
        """BDUSS方式登录，目前只支持这种类型的登录"""
        bduss = 'BDUSS=' + str(bduss)
        headers = {'Referer': 'http://tieba.baidu.com/',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
                   'Connection': 'keep-alive',
                   'cookie': bduss}
        req = urllib2.Request('http://tieba.baidu.com/dc/common/tbs', '', headers)
        response = urllib2.urlopen(req)
        # 获取提交后返回的信息
        content = response.read()
        json_ret = json.loads(content)
        islogin = json_ret['is_login']
        if islogin == 1:
            self.bduss = bduss
            return True
        return False

    def addReply(self, thread_id, content):
        """添加回帖"""
        forum = self.getForumByTid(thread_id)
        kw = str(forum['forum_name'])
        fid = str(forum['forum_id'])
        tid = str(thread_id)
        tbs = str(self._getTbs())
        content = str(content)
        post_data = [
           'ie=utf-8',
           'kw=' + kw,
           'fid=' + fid,
           'tid=' + tid,
           'tbs=' + tbs,
           'content=' + content
        ]
        headers = {'Referer': 'http://tieba.baidu.com/',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
                   'Connection': 'keep-alive',
                   'cookie': self.bduss}
        final_post_data = "&".join(post_data)
        req = urllib2.Request('http://tieba.baidu.com/f/commit/post/add', final_post_data, headers)
        response = urllib2.urlopen(req)
        # 获取提交后返回的信息
        content = response.read()
        return content

    def getThread(self, thread_id=4296390791, page=1, limit=30):
        """获取帖子信息"""
        tid = str(thread_id)
        page = str(page)
        limit = str(limit)
        post_data = [
           'kz=' + tid,
           'pn=' + page,
           'q_type=2',
           'rn=' + limit,
           'with_floor=1'
        ]
        return self._postByAndroidClient('http://c.tieba.baidu.com/c/f/pb/page', post_data)

    def getForumByTid(self, thread_id):
        """通过帖子号tid获取贴吧信息"""
        ret = self.getThread(thread_id=thread_id)
        forum = {}
        forum['forum_id'] = ret['forum']['id'].encode('gb2312')
        forum['forum_name'] = ret['forum']['name'].encode('gb2312')
        return forum

    def getForum(self, forum_name='', forum_id=0, page=1, result_number=1):
        """获取贴吧信息"""
        kw = str(forum_name)
        fid = str(forum_id)
        pn = str(page)
        rn = str(result_number)
        url = 'http://c.tieba.baidu.com/c/f/frs/page'
        post_data = [
            "kw=" + kw,
            # "fid=" + fid,
            "pn=" + pn,
            "q_type=2",
            "rn=" + rn,
            "with_group=1"
        ]
        ret = self._postByAndroidClient(url, post_data)
        return ret

    def _getTbs(self):
        """获取tbs，即贴吧csrf_token"""
        headers = {'Referer': 'http://tieba.baidu.com/',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
                   'Connection': 'keep-alive',
                   'cookie' : self.bduss}
        req = urllib2.Request('http://tieba.baidu.com/dc/common/tbs', '', headers)
        response = urllib2.urlopen(req)
        # 获取提交后返回的信息
        content = response.read()
        json_ret = json.loads(content)
        print content
        tbs = json_ret['tbs']
        return tbs

    def _postByAndroidClient(self, url='', post_data=[], headers={}):
        """通过客户端协议发送数据包"""
        post_data = [
            'BDUSS=' + self.bduss,
            '_client_id=wappc_1396611108603_817',
            '_client_type=2',
            '_client_version=5.7.0',
            '_phone_imei=642b43b58d21b7a5814e1fd41b08e2a6',
            'from=tieba'
        ] + post_data
        post_data.append("sign=" + self._getSignByPostData(post_data))
        # final_post_data = urllib.urlencode(post_data)
        final_post_data = "&".join(post_data)
        # 设置头部
        headers = dict({'Referer': 'http://tieba.baidu.com/',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
                   'Connection': 'keep-alive',
                   'cookie': self.bduss}, **headers)
        # req.add_header('Content-Type','application/x-www-form-urlencoded');
        # req.add_header('Referer','http://tieba.baidu.com/');
        # req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0');
        # req.add_header('Connection','keep-alive');
        # print final_post_data
        # 提交，发送数据
        req = urllib2.Request(url, final_post_data, headers)
        response = urllib2.urlopen(req)
        # 获取提交后返回的信息
        content = response.read()
        json_ret = json.loads(content)
        return json_ret

    def _getSignByPostData(self, post_data):
        """通过post数据获得sign校验码"""
        sign = hashlib.md5()
        # print "".join(post_data)
        sign.update("".join(post_data) + "tiebaclient!!!")
        return sign.hexdigest()
