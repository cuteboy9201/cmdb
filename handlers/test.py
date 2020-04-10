#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: YouShumin
@Date: 2020-03-25 12:03:11
@LastEditTime: 2020-04-02 14:43:10
@LastEditors: YouShumin
@Description: 测试文件
@FilePath: /cute_cmdb/handlers/test.py
'''
from oslo.web.requesthandler import MixinRequestHandler
from tornado import gen
from tornado.gen import coroutine
from task.publish import PublishMQ, HandlerSendMsg
from configs.setting import MQ_ANSIBLE_EXCHANGE, MQ_ANSIBLE_ROUTING_KEY
import logging
from oslo.web.route import route

LOG = logging.getLogger(__name__)


@route("/cmdb/test/setup/")
class TestHandler0323(MixinRequestHandler):
    @coroutine
    def get(self):
        LOG.debug(self.request_body)

        send_data = HandlerSendMsg()
        send_data.setup_handler("cfd0cc43-fc93-4403-b2d9-d5b2dac54c1f")
        self.send_ok(data="ok")
        return


@route("/cmdb/test/user/")
class TestHandlerUser(MixinRequestHandler):
    @coroutine
    def get(self):
        LOG.debug(self.request_body)
        send_data = HandlerSendMsg()
        req_data = dict(username="you2020")
        send_data.user_handler(msg_id="41a7bc14-85ca-4f77-9ad0-b8373627d1fa",
                               body=req_data)
        self.send_ok(data="ok")
        return