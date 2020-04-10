#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: YouShumin
@Date: 2019-11-20 17:15:56
@LastEditTime: 2020-03-25 12:06:27
@LastEditors: YouShumin
@Description: 
@FilePath: /cute_cmdb/handlers/userright.py
'''
import json
import logging

from configs.setting import (GETROLENAME_URI, GETUSERNAME_URI,
                             MQ_ANSIBLE_EXCHANGE, MQ_ANSIBLE_ROUTING_KEY,
                             MQ_URL, SYS_DEVAPP_USER, SYS_DEVOPS_USER,
                             SYS_SUDO_USER)
from dblib.crud import CmdbAdminUser, CmdbHost, CmdbSysUserAuth, CmdbUserRight
from forms.userright import GetUserRightInfo, UserRightPost
from oslo.form.form import form_error
from oslo.task.rabbitmq import TornadoAdapter
from oslo.util import create_id, dbObjFormatToJson
from oslo.web import httpclient
from oslo.web.requesthandler import MixinRequestHandler
from oslo.web.route import route
from task.publish import PublishMQ, test
from tornado import gen
from tornado.gen import coroutine
from tornado.options import options
from tornado.web import asynchronous
from utils.auth import WebRequestDataLog, check_request_permission
# from utils.mq import SendMsgToClient

LOG = logging.getLogger(__name__)

uuid_re = r"(?P<id>[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})"


@route("/cmdb/select/host")
class HostActiveHandler(MixinRequestHandler):
    @coroutine
    def get(self):
        reps_list = []
        host = CmdbHost()
        info = host.getAllByKeyValue("status", 1)
        for item in info:
            reps_list.append(dict(id=item.id, value=item.name))
        self.send_ok(data=reps_list)
        return


@route("/cmdb/select/user")
class UserHostHandler(MixinRequestHandler):
    @coroutine
    def get(self):
        req_list = []
        req_list.append(dict(id=SYS_SUDO_USER, value="sudo账号"))
        req_list.append(dict(id=SYS_DEVAPP_USER, value="运维账号"))
        req_list.append(dict(id=SYS_DEVOPS_USER, value="只读账号"))
        return self.send_ok(data=req_list)


@route("/cmdb/user/right")
class CmdbUserRightHandler(MixinRequestHandler):
    @WebRequestDataLog
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
        if code and msg:
            self.send_ok(data="添加成功")
            check_host_user_db = CmdbSysUserAuth()
            mq = PublishMQ()
            for item in eval(hostInfo):
                check_exist = check_host_user_db.check_exits(item, authUser)
                if not check_exist:
                    msg_data = {
                        "user": authUser,
                        "state": "present",
                        "task_type": "create_user"
                    }
                    mq.send_ansible_msg(body=dict(msg_id=item,
                                                  msg_data=msg_data,
                                                  msg_backable=False),
                                        hostinfo=item)
        else:
            self.send_fail(msg="添加失败")
        return

    @WebRequestDataLog
    def get(self):
        form = GetUserRightInfo(self)

        if form.is_valid():
            pageIndex = form.value_dict["pageIndex"]
            pageSize = form.value_dict["pageSize"]
            sortBy = form.value_dict["sortBy"]
            descending = form.value_dict["descending"]
        else:
            form_error(self, form)
            return

        UserRight = CmdbUserRight()

        totalCount, get_db = UserRight.getPage(pageIndex, pageSize, descending)
        rows = [dbObjFormatToJson(item) for item in get_db]
        if sortBy:
            rows = sorted(rows, key=lambda x: x[sortBy], reverse=descending)

        return_data = []
        for row in rows:
            data = {}
            sid = row.get("id")
            hostInfo = row.get("hostInfo")
            userInfo = row.get("userInfo")
            authUser = row.get("authUser")
            desc = row.get("authUser")
            roleInfo = row.get("roleInfo")
            data.setdefault("authUser", authUser)
            data.setdefault("desc", desc)
            data.setdefault("id", sid)
            host_data = ""
            ## 将HostId转为中文
            for host in eval(hostInfo):
                hostDB = CmdbHost()
                host_info = hostDB.getById(host)
                if host_data:
                    host_data = "{}, {}".format(host_data, host_info.name)
                else:
                    host_data = host_info.name
            data.setdefault("hostInfo", host_data)

            ## 将授权用户转为中文名字
            user_data = ""
            for user in eval(userInfo):
                req_data = dict(userId=user)
                req = httpclient.AsyncRequest(url=GETUSERNAME_URI,
                                              method="GET",
                                              **req_data)
                yield req.fetch()
                reps_data = req.resp

                if user_data:
                    user_data = "{}, {}".format(user_data,
                                                reps_data.get("data"))
                else:
                    user_data = reps_data.get("data")
            data.setdefault("userInfo", user_data)

            ## 将授权用户组转为中文名字
            role_data = ""
            for role in eval(roleInfo):
                req_data = dict(roleId=role)
                req = httpclient.AsyncRequest(url=GETROLENAME_URI,
                                              method="get",
                                              **req_data)
                yield req.fetch()
                reps_role_data = req.resp
                if role_data:
                    role_data = "{}, {}".format(role_data,
                                                reps_role_data.get("data"))
                else:
                    role_data = reps_role_data.get("data")
            data.setdefault("roleInfo", role_data)

            return_data.append(data)
        data = dict(totalCount=totalCount, rows=return_data)
        self.send_ok(data=data)
        return

    def delete(self):
        req_data = self.request_body()
        ids = req_data.get("ids", [])
        try:
            ids = json.loads(ids)

            for item in ids:
                userRight = CmdbUserRight()
                code, msg = userRight.delById(item)
                if not code:
                    LOG.warning("删除%s失败 %s", item, msg)
        except Exception as e:
            LOG.error(str(e))
            self.send_fail(msg="删除失败")
        else:
            self.send_ok(data="删除成功")
        return


@route("/cmdb/userright/{}".format(uuid_re))
class userRightIdHandler(MixinRequestHandler):
    def delete(self, id):
        """
            根据主键ID删除数据
        """
        userRight = CmdbUserRight()
        code, msg = userRight.delById(id)
        if code:
            self.send_ok(data="")
        else:
            self.send_fail(msg=msg)
        return
