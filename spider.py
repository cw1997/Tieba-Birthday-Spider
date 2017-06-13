#! /usr/bin/env python
# -*- coding: utf-8 -*-

# spider  爬虫主文件
# version 0.1.0
# author:changwei [867597730@qq.com]
# website: https://github.com/cw1997
# data:2017-06-12 05:09:53

# runtime env:windows 7 64bit + python 2.7.10


import threading
import Queue
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pymongo

from SpiderUtil import *
from config import *


class ForumWorker(threading.Thread):
    """通过贴吧名字抓取吧友id"""
    """该类依赖TiebaSpider"""

    def __init__(self, forum, forum_page_queue, member_queue):
        threading.Thread.__init__(self)
        self.forum_name = forum['forum_name']
        self.forum_page_queue = forum_page_queue
        self.member_queue = member_queue
        self.tieba_spider = TiebaSpider()

    def run(self):
        while True:
            page = self.forum_page_queue.get()
            print('fetch members at page : ' + str(page))
            members = self.tieba_spider.fetchMembersByForum(self.forum_name, page)
            # 抓取出错重新丢回队列
            if len(members)==0 :
                self.forum_page_queue.put(page)
            else:
                # 遍历member的username并加入member队列
                for username in members:
                    # username = str(username)
                    self.member_queue.put(username)
                    print('put the member to member_queue : ' + username)
                    # signals to queue job is done
                self.forum_page_queue.task_done()


class MemberWorker(threading.Thread):
    """通过贴吧名字抓取吧友id"""
    """该类依赖TiebaSpider"""

    def __init__(self, forum, member_queue, member_collection):
        threading.Thread.__init__(self)
        self.forum = forum
        self.member_queue = member_queue
        self.member_collection = member_collection
        self.tieba_spider = TiebaSpider()

    def run(self):
        while True:
            username = self.member_queue.get()
            print('fetch user infomation by username : ' + username)
            detail = self.tieba_spider.fetchDetailByUsername(username)
            # 抓取出错重新丢回队列
            if len(detail)==0 :
                self.member_queue.put(username)
            else:
                print('store user infomation to the database : ' + username)
                detail['forum'] = self.forum
                self.member_collection.insert(SpiderUtil.formatDetail(detail))
                # signals to queue job is done
            self.member_queue.task_done()


def main():
    forum_name = config['forum_name']
    # 对应的贴吧id，此处为系统自动获取函数，无需修改
    util = SpiderUtil(forum_name)
    forum_id = util.getFidByFname()
    thread_num = config['thread_num']
    pages = config['pages']

    client = pymongo.MongoClient(config['ip'], config['port'])
    db = client.get_database(config['database'])
    mongodb_username = config['username']
    mongodb_password = config['password']
    if mongodb_username != '':
        db.authenticate(mongodb_username, mongodb_password)
    member_collection = db[forum_id]
    forum_collection = db['forum']
    # 此处未做并发控制，如果严谨考虑，需要做唯一索引：createIndex({forum_name:1},{unique:true})
    forum_result = forum_collection.count({'forum_name': forum_name, 'forum_id': forum_id})
    if forum_result == 0:
        forum_collection.insert({'forum_name': forum_name, 'forum_id': forum_id})

    forum_page_queue = Queue.Queue()
    member_queue = Queue.Queue()

    member_number = int(util.getRankNumByFname())
    print 'total member : %d' % member_number
    for page in pages:
        page = int(page)
        # 昌维吧会员数196，也就是只有10页，所以要过滤掉大于10的page_num
        if page <= (member_number + 20) / 20:
            forum_page_queue.put(page)

    forum = {}
    forum['forum_id'] = forum_id
    forum['forum_name'] = forum_name

    pages_num = forum_page_queue.qsize()
    task_start_time = time.time()
    for i in range(thread_num):
        t = ForumWorker(forum, forum_page_queue, member_queue)
        t.setDaemon(True)
        t.start()
    forum_page_queue.join()
    print 'fetch member complete in : ' + str(time.time() - task_start_time) + ' s'

    member_num = member_queue.qsize()
    task_start_time = time.time()
    for i in range(thread_num):
        t = MemberWorker(forum, member_queue, member_collection)
        t.setDaemon(True)
        t.start()
    member_queue.join()

    print '------------------------------------------------------------'
    print 'member_number : %d' % member_num
    print 'pages_number : %d' % pages_num
    print 'fetch member detail complete in : ' + str(time.time() - task_start_time) + ' s'
    print '------------------------------------------------------------'
    print 'thanks for using the tieba birthday spider.'
    print 'code by changwei [867597730@qq.com] https://github.com/cw1997.'


if __name__ == '__main__':
    main()


