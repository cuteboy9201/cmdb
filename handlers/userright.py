#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: YouShumin
@Date: 2019-11-20 17:15:56
@LastEditTime : 2019-12-27 17:55:24
@LastEditors  : YouShumin
@Description: 
@FilePath: /cmdb/handlers/userright.py
'''
import logging
import json
from utils.mq import SendMsgToClient
from oslo.form.form import form_error
from oslo.util import dbObjFormatToJson
from oslo.web.requesthandler import MixinRequestHandler
from oslo.web.route import route
from tornado.gen import coroutine
from forms.userright import UserRightPost
from dblib.crud import CmdbHost, CmdbAdminUser, CmdbUserRight, CmdbSysUserAuth
from utils.auth import check_request_permission
from tornado.options import options
from configs.setting import MQ_ANSIBLE_EXCHANGE, MQ_ANSIBLE_ROUTING_KEY
from configs.setting import SYS_APP_USER, SYS_SUDO_USER, SYS_READ_ONLY_USER
from utils.rabbitmq_rdapter import TornadoAdapter
from configs.setting import MQ_URL, MQ_ANSIBLE_EXCHANGE, MQ_ANSIBLE_ROUTING_KEY
LOG = logging.getLogger(__name__)


@route("/cmdb/1234")
class TESTHANDLER(MixinRequestHandler):
    @coroutine
    def get(self):
        mq = TornadoAdapter(MQ_URL)
        body = {"hello": "world!!!"}
        print("xxx")
        mq.publish(MQ_ANSIBLE_EXCHANGE, MQ_ANSIBLE_ROUTING_KEY, body)
        self.send_ok(data="")
        return


@route("/cmdb/select/host")
class HostActiveHandler(MixinRequestHandler):
    @coroutine
    def get(self):
        reps_list = []
        host = CmdbHost()
        info = host.getAllByKeyValue("status", 1)
        for item in info:
            reps_list.append(dict(id=item.id, value=item.name))
        return self.send_ok(data=reps_list)
        return


@route("/cmdb/select/user")
class UserHostHandler(MixinRequestHandler):
    @coroutine
    def get(self):
        req_list = []
        req_list.append(dict(id=SYS_SUDO_USER, value="sudo账号"))
        req_list.append(dict(id=SYS_APP_USER, value="运维账号"))
        req_list.append(dict(id=SYS_READ_ONLY_USER, value="只读账号"))
        return self.send_ok(data=req_list)


@route("/cmdb/user/right")
class CmdbUserRightHandler(MixinRequestHandler):
    @coroutine
    def post(self):
        form = UserRightPost(self)
        if form.is_valid():
            hostInfo = form.value_dict["hostInfo"]
            authUser = form.value_dict["authUser"]
            userInfo = form.value_dict["userInfo"]
            roleInfo = form.value_dict["roleInfo"]
            desc = form.value_dict["desc"]
        else:
            form_error(self, form)
            return
        if not userInfo and not roleInfo:
            self.send_fail(msg="roleInfo, userInfo不能同时为空")
            return

        DB = CmdbUserRight()
        code, msg = DB.post(hostInfo, authUser, userInfo, roleInfo, desc)
        if code:
            self.send_ok(data="添加成功")
            check_host_user_db = CmdbSysUserAuth()
            mq = SendMsgToClient(self.application.mq_server,
                                 MQ_ANSIBLE_EXCHANGE, MQ_ANSIBLE_ROUTING_KEY)
            for item in eval(hostInfo):
                check_exist = check_host_user_db.check_exits(item, authUser)
                if not check_exist:
                    args = {"user": authUser, "state": "present"}
                    mq.send_create_user(item, args)
        else:
            self.send_fail(msg="添加失败")
        return