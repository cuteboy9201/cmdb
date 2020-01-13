#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: YouShumin
@Date: 2019-12-31 11:00:47
@LastEditTime : 2020-01-09 03:26:12
@LastEditors  : YouShumin
@Description: 
@FilePath: /cmdb/task/publish.py
'''
import json
import logging

from configs.setting import (MQ_ANSIBLE_EXCHANGE, MQ_ANSIBLE_ROUTING_KEY,
                             MQ_SERVER_EXCHANGE, MQ_SERVER_ROUTING_KEY, MQ_URL)
from dblib.crud import CmdbAdminUser, CmdbHost, CmdbHostAuth, CmdbSysUserAuth
from oslo.task.rabbitmq import TornadoAdapter
from oslo.util import create_id
from tornado.gen import coroutine
from dblib.crud import CmdbSysUserAuth

logging.getLogger(__name__)


class PublishMQ(object):
    def __init__(self):
        self.mq = TornadoAdapter(MQ_URL)
        self.allow_send = False

    def get_auth(self, hostid):
        host_db = CmdbHost()
        host_info = host_db.getById(hostid)
        if host_info:
            auth_db = CmdbAdminUser()
            auth_info = auth_db.getById(host_info.authInfo)
        if auth_info and host_info:
            self.hostauthinfo = [
                dict(
                    host=host_info.connectHost,
                    port=host_info.connectPort,
                    user=auth_info.sshUser,
                    ansible_ssh_private_key_file=auth_info.sshKey,
                    password=auth_info.sshPass,
                    sudo_user="" if auth_info.sshKey else auth_info.sshUser,
                    sudo_pass="" if auth_info.sshKey else auth_info.sudoPass,
                )
            ]

    @coroutine
    def send_ansible_msg(self, body=None, hostinfo=None):
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
        self.get_auth(hostinfo)
        if self.hostauthinfo:
            data = body
            data["hostinfo"] = self.hostauthinfo
            logging.info("rabbit publish body: %s", data)
            return_data = yield self.mq.rpc(MQ_ANSIBLE_EXCHANGE,
                                            MQ_ANSIBLE_ROUTING_KEY,
                                            json.dumps(data),
                                            timeout=10,
                                            ttl=2)
            if return_data:
                self.rpc_return_handler(return_data)

    def rpc_return_handler(self, body):
        body = json.loads(body)
        msg_task = body.get("msg_task", None)
        if msg_task == "user":
            self.user_return(body)

    def user_return(self, body):
        try:
            msg_data = body.get("msg_data")
            hostId = body.get("msg_id")
            authUser = msg_data.get("user")
            authPass = msg_data.get("password")
            authPriKey = msg_data.get("sshPirKey")
            authPubKey = msg_data.get("sshPubKey")
            if hostId and authPass and authUser and authPriKey and authPubKey:
                DB = CmdbSysUserAuth()
                code, mid = DB.post(hostId, authUser, authPass, authPriKey,
                                    authPubKey)
                print(code)
                if code == "exist":
                    logging.error("给%s主机添加账号失败,已经存在的记录%s", hostId, mid)
                elif code:
                    logging.info("给%s主机添加账号%s成功, 记录ID%s", hostId, authUser,
                                 mid)

        except Exception as e:
            logging.error(str(e))
            logging.error("给主机%s添加账号%s失败", hostId, authUser)


def test():
    body = {
        "msg_id": create_id(),
        "msg_data": dict(task="setup"),
        "msg_backable": False,
        "msg_return": {}
    }
    mq = PublishMQ()
    mq.send_ansible_msg(body)
