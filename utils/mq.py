#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-12-18 10:03:38
@LastEditors  : YouShumin
@LastEditTime : 2019-12-27 14:57:30
@Description:
'''
import datetime
import json
import logging

import pika
from configs.setting import (MQ_ANSIBLE_EXCHANGE, MQ_ANSIBLE_ROUTING_KEY,
                             MQ_SERVER_EXCHANGE, MQ_SERVER_ROUTING_KEY)
from dblib.crud import CmdbAdminUser, CmdbHost, CmdbHostAuth, CmdbSysUserAuth
from oslo.task import mq_server
from tornado.web import Application

LOG = logging.getLogger(__name__)


class RabbitServer(mq_server.PikaPublisher):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.props = pika.BasicProperties(reply_to=self.ROUTING_KEY,
    #                                       message_id=self.EXCHANGE)
    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
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

    def get_hostinfo(self, hostId):
        AuthDB = CmdbAdminUser()
        HostDb = CmdbHost()
        hostinfo = HostDb.getById(hostId)
        authinfo = AuthDB.getById(hostinfo.authInfo)
        hostauthinfo = []
        if authinfo and hostinfo:
            hostauthinfo = [
                dict(host=hostinfo.connectHost,
                     port=hostinfo.connectPort,
                     user=authinfo.sshUser,
                     ansible_ssh_private_key_file=authinfo.sshKey,
                     password=authinfo.sshPass,
                     sudo_user="" if authinfo.sshKey else authinfo.sshUser,
                     sudo_pass="" if authinfo.sshKey else authinfo.sudoPass)
            ]
        return hostinfo.id, hostauthinfo

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
                                   msg_auth=hostauthinfo,
                                   msg_return=True)

            self.mq.send_msg(json.dumps(mq_request_data), self.exchange,
                             self.routing_key)

    def send_create_user(self, hostinfo, args):
        LOG.debug("send_create_user: {}".format(hostinfo))
        msg_id, hostauth = self.get_hostinfo(hostinfo)
        if hostauth:
            mq_request_data = dict(msg_id=msg_id,
                                   msg_task="user",
                                   msg_auth=hostauth,
                                   msg_return=True,
                                   msg_args=args)
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
        elif self.msg_task == "user":
            self.api_user()
        else:
            print(self.msg_data)

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

    def api_user(self):
        LOG.info("start handler sys-info: %s", self.msg_id)
        DB = CmdbSysUserAuth()
        user = self.msg_data.get("user", None)
        check_exist = ""
        if user and self.msg_id:
            check_exist = DB.check_exits(self.msg_id, user)
        if not check_exist:
            LOG.info("信息存在")
            mq_server = RabbitServer()
            mq = SendMsgToClient(mq_server, MQ_ANSIBLE_EXCHANGE,
                                 MQ_ANSIBLE_ROUTING_KEY)
            mq.send_create_user(self.msg_id, {
                "user": "youshumin007",
                "state": "present"
            })
        else:
            try:
                code, msg = DB.post(self.msg_id,
                                    authUser=self.msg_data["user"],
                                    authPass=self.msg_data["password"],
                                    authPriKey=self.msg_data["sshPirKey"],
                                    authPubKey=self.msg_data["sshPubKey"])
            except Exception as e:
                LOG.error(e)
