#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: YouShumin
@Date: 2019-12-31 11:01:01
@LastEditTime : 2019-12-31 15:22:35
@LastEditors  : YouShumin
@Description: 处理接收到的rabbitmq消息
@FilePath: /cmdb/task/receive_handler.py
'''
import json
import logging
logging.getLogger(__name__)


class ReceiveHandle(object):
    def __init__(self, body):
        try:
            self.body = json.loads(body)
            msg_id = self.body.get("msg_id")
            msg_data = self.body.get("msg_data")
            msg_backable = self.body.get("msg_backable")
            msg_return = self.body.get("msg_return")
            logging.info("recevie msg_data: %s", msg_data)
        except Exception as e:
            self.body = dict()
            logging.info("receive data %s", body)
            logging.error(e)
