#! /usr/bin/env python
# -*- coding: utf-8 -*-

# config  配置文件
# version 0.1.0
# author:changwei [867597730@qq.com]
# website: https://github.com/cw1997
# data:2017-06-12 23:39:45

# runtime env:windows 7 64bit + python 2.7.10

config = {}

# ---------- MongoDB ---------- #
# 暂时只支持mongodb进行持久化存储，爬虫使用pymongo库进行操作。
# 安全提示：如果未给数据库加密码，请注意关闭MongoDB的公网访问权限，
# 如果是使用云主机经典网络，请注意设置防火墙和MongoDB所在端口有关的入站规则，防止MongoDB被非法访问造成主机被黑客入侵。
# 如果必须需要外网连接MongoDB，请注意给数据库设置密码。
# MongoDB数据库连接IP
config['ip'] = 'localhost'
# MongoDB数据库连接密码
config['port'] = 27017
# MongoDB数据库名字
config['database'] = 'tieba_birthday_spider'
# MongoDB数据库密码（默认情况下无安全验证请留空）
config['username'] = ''
# MongoDB数据库密码（默认情况下无密码请留空）
config['password'] = ''

# ---------- network ---------- #
# requests库请求超时（单位：秒）
config['timeout'] = 6

# ---------- spider ---------- #
# 要抓取的贴吧名称（不要带“吧”字，比如说要抓取昌维吧，直接输入昌维即可）
config['forum_name'] = '昌维'
# 线程数量，根据自己网络环境和硬件配置设置
config['thread_num'] = 50
# 抓取页码集合，一页是20条用户记录，可用range生成器批量生成连续的页码，起始页码为1，所以range第一个参数不能小于1.
config['pages'] = range(1, 1000)

# ---------- post ---------- #
# 发帖帐号的bduss，一般为192位，使用list进行存储多个账号轮流发送防止验证码，请将下列示例bduss修改为自己的bduss
# bduss获取方法请自行百度
config['bduss'] = [
    'bduss1',
    'bduss2',
    'bduss3',
    'bduss4',
    'bduss5'
]
# 两次发帖之间的间隔时间（单位：秒），该时间调的越长，出现验证码的概率越少
# 但是如果该吧每天过生日的会员数量过多，比如说一个关注量百万级别的贴吧，
# 按照抽屉原理计算可能会有上千人同一天过生日，则需要适当缩短该时间，并且加入更多的发帖帐号bduss，用于快速发送，
# 这样可以尽可能延长同一帐号两次发帖之间的间隔
config['wait_time'] = 60
# 帖子id，比如说你从地址栏复制的帖子链接为https://tieba.baidu.com/p/4296390791，那么帖子id就为 4296390791
config['post_thread_id'] = '4296390791'
# 发送祝福的吧友所在贴吧，比如说你想给昌维吧的所有当天过生日的吧友发送祝福，那么此处填写“昌维”即可
config['post_forum_name'] = '昌维'
# 祝福语录，发帖时会随机选择并追加至回帖内容末尾
config['wish'] = [
    '新的一岁祝你顺顺利利，每天开心。',
    '愿这特殊的日子里，你的每时每刻都充满欢乐。',
    '愿你在新的一岁，一切的快乐，一切的幸福，一切的温馨，一切的好运永远围绕在你身边。',
    '因为你的降临，这一天成了一个美丽的日子，从此世界，便多了一抹诱人的色彩。',
    '岁月总是愈来愈短，生日总是愈来愈快，友情总是愈来愈浓，我的祝福也就愈来愈深，愿你的每一天都如画一样的美丽。'
]

