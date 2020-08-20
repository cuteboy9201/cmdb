#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: YouShumin
@Date: 2019-11-20 17:15:56
@LastEditTime: 2020-06-11 14:51:30
@LastEditors: YouShumin
@Description: 
@FilePath: /cute_cmdb/configs/dev_cfg.py
'''

# 测试时候的默认设置
BD_ECHO = True
REQUEST_URI = "http://dev.code.cn"

DB_HOST = "mysql+pymysql://rbac:123456@192.168.2.69:12502/cute_rbac?charset=utf8"
DB_NAME = "cmdb"
MQ_URL = "amqp://admin:admin@192.168.2.132:5672/my_vhost"

ALLOW_HOST = ["*"]
LOGFILE = "/work_app/logs/dev_rbac.log"
