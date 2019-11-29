#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-12 16:05:49
@LastEditors: Youshumin
@LastEditTime: 2019-11-29 11:06:55
@Description: 
'''
# RBAC_DB = "mysql+pymysql://you:123456@clouddata20181111.mysql.rds.aliyuncs.com:1234/rbac?charset=utf8"
# RBAC_DB = "mysql+pymysql://rbac:123456@192.168.2.69:12502/cute_rbac?charset=utf8"
# RBAC_DB_ECHO = True
# ADMIN_LIST = ["youshumin", "superuser"]

DB_HOST = "mysql+pymysql://rbac:123456@192.168.2.69:12502/cute_rbac?charset=utf8"
BD_ECHO = False
DB_NAME = "cmdb"
CHECK_PERMISSION_URI = "http://192.168.2.108:18080/rbac/check_permission"