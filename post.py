#! /usr/bin/env python
# -*- coding: utf-8 -*-

# post  祝福贴发送
# version 0.1.0
# author:changwei [867597730@qq.com]
# website: https://github.com/cw1997
# data:2017-06-13 00:07:18

# runtime env:windows 7 64bit + python 2.7.10

import time
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pymongo

from TiebaUtil import *
from config import *


def main():
    tieba_util = TiebaUtil()
    bduss_list = config['bduss']
    bduss_list_num = len(bduss_list)
    # bduss检测
    all_bduss_is_logout = True
    for bduss in bduss_list:
        if tieba_util.login(bduss):
            all_bduss_is_logout = False
    # 如果所有bduss都失效，直接退出脚本
    if all_bduss_is_logout == True:
        exit(1)

    client = pymongo.MongoClient(config['ip'], config['port'])
    db = client.get_database(config['database'])
    mongodb_username = config['username']
    mongodb_password = config['password']
    if mongodb_username != '':
        db.authenticate(mongodb_username, mongodb_password)
    forum_collection = db['forum']
    forum_result = forum_collection.find_one({'forum_name': config['post_forum_name']})
    forum_id = forum_result['forum_id']

    y = int(time.strftime("%Y"))
    # 通过二次数据类型转换是为了移除单位数日期前面带的0，也就是将06转换为6
    m = str(int(time.strftime("%m")))
    d = str(int(time.strftime("%d")))

    member_collection = db[forum_id]
    find = {'birthday.month': m, 'birthday.day': d}
    member_list = member_collection.find(find)
    member_count =  member_collection.count(find)

    thread_id = config['post_thread_id']
    post_thread_id = config['post_thread_id']

    # 用于后续计算取得bduss下标
    i = 0
    wait_time = config['wait_time']
    for member in member_list:
        # print member
        content = buildContent(member, member_count, y)
        # print content
        bduss = bduss_list[i % bduss_list_num]
        islogin = tieba_util.login(bduss)
        # 当帐号登录失败则换下一个帐号登录
        while islogin == False:
            i = i + 1
            bduss = bduss_list[i % bduss_list_num]
            islogin = tieba_util.login(bduss)
        # print i, bduss
        tieba_util.addReply(post_thread_id, content)
        # i自增用于顺序取得下一条bduss帐号凭据
        i = i + 1
        time.sleep(wait_time)


def buildContent(member, member_count, now_year):
    """回复内容模版构造，member为祝福对象的dict，member_count为当天过生日的总人数，用户可根据自己需要自行修改"""
    content = ''
    gender = ''
    member_gender = member[u'gender']
    member_username = member[u'username']
    member_birthday_year = int(member[u'birthday'][u'year'])
    if member_gender == u'男':
        gender = '帅帅哒的汉纸'
    elif member_gender == u'女':
        gender = '美美哒的妹纸'
    else:
        gender = '吧友'
    wish_num = len(config['wish'])
    content = '祝@%s %s生日快乐哈！今天是%s，也是你%d岁的生日，在%s吧内共有%s位吧友和你同样幸运的降临在了这个神奇的日子' \
              '，让我们一起祝福他们破壳日快乐！！！%s' % \
              (member_username, gender, time.strftime('%Y年%m月%d日'), now_year - member_birthday_year, config['post_forum_name'], \
               member_count, config['wish'][random.randint(0, wish_num - 1)])
    return content


if __name__ == '__main__':
    main()