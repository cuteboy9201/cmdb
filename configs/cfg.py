#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: YouShumin
@Date: 2020-01-13 16:56:52
@LastEditTime: 2020-03-25 11:22:55
@LastEditors: YouShumin
@Description: 
@FilePath: /cute_cmdb/configs/cfg.py
'''
DB_HOST = "mysql+pymysql://rbac:123456@192.168.2.69:12502/cute_rbac?charset=utf8"
BD_ECHO = False
DB_NAME = "cmdb"
REQUEST_URI = "http://dev.code.cn"
CHECK_PERMISSION_URI = "http://192.168.2.132:3001/rbac/check_permission"
MQ_URL = "amqp://admin:admin@192.168.2.132:5672/my_vhost"
ALLOW_HOST = ["*"]
LOGFILE = "/work_app/logs/dev_rbac.log"