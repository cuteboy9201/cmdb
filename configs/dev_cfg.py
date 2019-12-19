#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-12 16:05:49
@LastEditors  : Please set LastEditors
@LastEditTime : 2019-12-18 15:41:03
@Description: 
'''
# RBAC_DB = "mysql+pymysql://you:123456@clouddata20181111.mysql.rds.aliyuncs.com:1234/rbac?charset=utf8"
# RBAC_DB = "mysql+pymysql://rbac:123456@192.168.2.69:12502/cute_rbac?charset=utf8"
# RBAC_DB_ECHO = True
# ADMIN_LIST = ["youshumin", "superuser"]

DB_HOST = "mysql+pymysql://rbac:123456@192.168.2.69:12502/cute_rbac?charset=utf8"
BD_ECHO = False
DB_NAME = "cmdb"
CHECK_PERMISSION_URI = "http://192.168.2.132:18080/rbac/check_permission"

MQ_URL = "amqp://admin:admin@192.168.2.132:5672/my_vhost"
# RABBIT_SERVER
MQ_SERVER_QUEUE = "return_cmdb_queue"
MQ_SERVER_EXCHANGE = "return_cmdb_exchange"
MQ_SERVER_ROUTING_KEY = "return_cmdb.key"

MQ_ANSIBLE_EXCHANGE = "ansible_exchange"
MQ_ANSIBLE_ROUTING_KEY = "ansible.client"
