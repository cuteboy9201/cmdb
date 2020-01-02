#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: YouShumin
@Date: 2019-11-20 17:15:56
@LastEditTime : 2019-12-31 15:21:32
@LastEditors  : YouShumin
@Description: 
@FilePath: /cmdb/configs/dev_cfg.py
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
MQ_SERVER_QUEUE = "cute_cmdb_queue"
MQ_SERVER_EXCHANGE = "cute_cmdb_exchange"
MQ_SERVER_ROUTING_KEY = "cute_cmdb_routing_key"

MQ_ANSIBLE_EXCHANGE = "cute_ansible_exchange"
MQ_ANSIBLE_ROUTING_KEY = "cute_ansible_routing_key"

# 具有sudo权限应用 [sudo]
SYS_SUDO_USER = "kw_sudo"
# 项目应用 属公司开发项目 【运维权限】
SYS_APP_USER = "kw_app"
# 只读账号 一般给开发查看日志使用 【开发权限】
SYS_READ_ONLY_USER = "kw_scan"
# LNMP应用安装使用账户 【不具有登陆权限】
SYS_WWW_USER = "kw_www"
# 基础应用安装redis、memcache、mysql... 【不具有登陆权限】
SYS_BASE_USER = "kw_base"
