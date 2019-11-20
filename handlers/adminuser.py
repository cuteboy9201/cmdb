#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-19 14:34:42
@LastEditors: Youshumin
@LastEditTime: 2019-11-20 14:58:07
@Description: 
'''

import logging
from oslo.web.requesthandler import MixinRequestHandler
from oslo.web.route import route
from tornado.gen import coroutine

LOG = logging.getLogger(__name__)


@route("/cmdb/adminuser/")
class AdminUserBaseHandler(MixinRequestHandler):
    @coroutine
    def get(self):
        '''
        @description: 
        @param {type} 
        @return: 
        '''
        self.send_ok(data="")
        return

    @coroutine
    def post(self):
        '''
        @description: 
        @param {type} 
        @return: 
        '''
        req_data = self.request_body()
        LOG.debug(req_data)
        self.send_ok(data="")
        return


@route("/cmdb/(.*)")
class AllHandler(MixinRequestHandler):
    @coroutine
    def get(self):
        req_data = self.request_body()
        LOG.debug(req_data)
        return self.send_ok(data="")

    @coroutine
    def post(self):
        req_data = self.request_body()
        LOG.debug(req_data)
        return self.send_ok(data="")