#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: YouShumin
@Date: 2019-12-31 11:00:47
@LastEditTime : 2019-12-31 15:47:55
@LastEditors  : YouShumin
@Description: 
@FilePath: /cmdb/task/publish.py
'''
import json

from configs.setting import (MQ_ANSIBLE_EXCHANGE, MQ_ANSIBLE_ROUTING_KEY,
                             MQ_SERVER_EXCHANGE, MQ_SERVER_ROUTING_KEY, MQ_URL)
from oslo.task.rabbitmq import TornadoAdapter
from oslo.util import create_id
from dblib.crud import CmdbAdminUser, CmdbHost, CmdbHostAuth, CmdbSysUserAuth
import logging

logging.getLogger(__name__)


class PublishMQ(object):
    def __init__(self):
        self.mq = TornadoAdapter(MQ_URL)
        self.allow_send = False

    def send_ansible_msg(self, body=None, hostinfo=None, authinfo=None):
        """
            发送消息给ansible队列处理
            body: {
                msg_id: str ----,
                msg_data: {} 消息内容,
                msg_backable: bool, 是否需要回复
                msg_return: {
                    return_exchange: "",
                    return_routing_key: "",
                }
            }
        """
        auth_db = CmdbAdminUser()
        auth_info = auth_db.getById(authinfo)
        if auth_info:
            hostauthinfo = [
                dict(
                    host=hostinfo["host"],
                    port=hostinfo["port"],
                    user=auth_info.sshUser,
                    ansible_ssh_private_key_file=auth_info.sshKey,
                    password=auth_info.sshPass,
                    sudo_user="" if auth_info.sshKey else auth_info.sshUser,
                    sudo_pass="" if auth_info.sshKey else auth_info.sudoPass,
                )
            ]
            msg_id = create_id()
            data = body
            data["hostinfo"] = hostauthinfo
            msg_backable = False
            self.body = dict(msg_id=msg_id,
                             msg_data=data,
                             msg_backable=msg_backable)
            logging.info("rabbit publish body: %s", self.body)
            self.mq.publish(MQ_ANSIBLE_EXCHANGE, MQ_ANSIBLE_ROUTING_KEY,
                            json.dumps(self.body))

    def send_cmdb_msg(self, body):
        if self.allow_send:
            self.mq.publish(MQ_SERVER_EXCHANGE, MQ_SERVER_ROUTING_KEY,
                            json.dumps(body))


def test():
    body = {
        "msg_id": create_id(),
        "msg_data": dict(task="setup"),
        "msg_backable": False,
        "msg_return": {}
    }
    mq = PublishMQ()
    mq.send_ansible_msg(body)
