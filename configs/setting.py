#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-10-11 11:24:53
@LastEditors: YouShumin
@LastEditTime: 2020-03-25 11:28:39
@Description: 
'''

import os

debug = os.environ.get("RUN_ENV")

if debug == "prod":
    from configs.cfg import *
else:
    from configs.dev_cfg import *

PATH_APP_ROOT = os.path.abspath(
    os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))))

COOKIE_SECRET = "0wEE^@!TKGwbC0p@nyY4*Cm*8ojzulHC48HT620YJl^zE6qE"
PROJECT_NAME = "cute_cmdb"
HOST = "0.0.0.0"
PORT = 3000

GETUSERNAME_URI = REQUEST_URI + "/rbac/user/getname"  # 获取用户中文名字
GETROLENAME_URI = REQUEST_URI + "/rbac/role/getname"  # 获取角色中文名字
CHECK_PERMISSION_URI = REQUEST_URI + "/rbac/check_permission"  # 检验权限

# 作为rq_server配置
MQ_SERVER_QUEUE = "cute_cmdb_queue"
MQ_SERVER_EXCHANGE = "cute_cmdb_exchange"
MQ_SERVER_ROUTING_KEY = "cute_cmdb_routing_key"
# ansible_rq_相关配置
MQ_ANSIBLE_EXCHANGE = "cute_ansible_exchange"
MQ_ANSIBLE_ROUTING_KEY = "cute_ansible_routing_key"

##### 平台提供的创建的默认用户名字
# 具有sudo权限应用 [sudo]
SYS_SUDO_USER = "admin_user"
# 项目应用 属公司开发项目 【运维权限】
SYS_DEVAPP_USER = "devapp_user"
# 只读账号 一般给开发查看日志使用 【开发权限】
SYS_DEVOPS_USER = "devops_user"
# LNMP应用安装使用账户 【不具有登陆权限】
SYS_WWW_USER = "lnmp_user"
# 基础应用安装redis、memcache、mysql... 【不具有登陆权限】
SYS_BASEAPP_USER = "baseapp_user"