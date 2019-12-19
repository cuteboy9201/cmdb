#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-12-18 10:03:38
@LastEditors  : Youshumin
@LastEditTime : 2019-12-18 12:03:16
@Description:
'''
import datetime
import json
import logging

import pika
from configs.setting import MQ_SERVER_EXCHANGE, MQ_SERVER_ROUTING_KEY
from dblib.crud import CmdbAdminUser, CmdbHost
from oslo.task import mq_server

LOG = logging.getLogger(__name__)


class RabbitServer(mq_server.PikaPublisher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.props = pika.BasicProperties(reply_to=self.ROUTING_KEY,
                                          message_id=self.EXCHANGE)

    def handler_body(self, msg):
        LOG.info("返回到cmdb的消息: {}".format(msg))
        ReturnInfoHandler(msg)
        return True


class SendMsgToClient(object):
    def __init__(self, mq, exchange, routing_key):
        self.mq = mq
        self.exchange = exchange
        self.routing_key = routing_key

    def send_sysinfo(self, hostinfo, authid):
        auth_db = CmdbAdminUser()
        auth_info = auth_db.getById(authid)

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
            mq_request_data = dict(msg_id=hostinfo["id"],
                                   msg_task="setup",
                                   msg_data=hostauthinfo,
                                   msg_return=True)

            self.mq.send_msg(json.dumps(mq_request_data), self.exchange,
                             self.routing_key)


class ReturnInfoHandler(object):
    def __init__(self, msg):
        self.return_msg = json.loads(msg)
        self.msg_task = self.return_msg.get("msg_task", None)
        self.msg_id = self.return_msg.get("msg_id", None)
        self.msg_data = self.return_msg.get("msg_data", [])
        if self.msg_task == "setup":
            self.task_sysinfo()

    def task_sysinfo(self):
        LOG.info("start handler sys-info: %s", self.msg_id)
        host_db = CmdbHost()
        hostinfo = host_db.getById(self.msg_id)
        try:
            for item in self.msg_data:
                host_data = item.get(hostinfo.connectHost)
                if host_data and host_data["code"] == 0:
                    hostinfo.hostname = host_data["hostname_raw"]
                    hostinfo.address = host_data["all_ipv4_address"]
                    hostinfo.sysinfo = "{} {} {}C{}".format(
                        host_data["os"], host_data["os_version"],
                        host_data["cpu_count"], host_data["memory"])
                    hostinfo.hdinfo = "{}".format(host_data["disk_total"])
                    hostinfo.updateTime = datetime.datetime.now()
                    hostinfo.status = 1
                host_db.session.commit()
        except Exception as e:
            LOG.warning("task_sysinfo return data handler fail: %s", e)
