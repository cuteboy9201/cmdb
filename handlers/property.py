#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-20 17:15:56
@LastEditors  : YouShumin
@LastEditTime : 2019-12-31 15:48:19
@Description: 
'''
import logging
import json
from utils.mq import SendMsgToClient
from oslo.form.form import form_error
from oslo.util import dbObjFormatToJson
from oslo.web.requesthandler import MixinRequestHandler
from oslo.web.route import route
from tornado.gen import coroutine
from forms.property import BasePostForm, GETBaseForm, PUTBaseForm
from dblib.crud import CmdbHost, CmdbAdminUser
from utils.auth import check_request_permission
from tornado.options import options
from configs.setting import MQ_ANSIBLE_EXCHANGE, MQ_ANSIBLE_ROUTING_KEY
from task.publish import PublishMQ
LOG = logging.getLogger(__name__)

uuid_re = "(?P<id>[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})"


@route("/cmdb/property/")
class BaseHandler(MixinRequestHandler):
    """
        请求path中不带uuid的请求
        
        post: 添加一台资产信息
        get: 获取资产信息列表
        delete: 根据ids列表删除资产
        put: 修改一台资产信息
    """
    @check_request_permission()
    @coroutine
    def post(self):
        LOG.debug(self.request_body())

        form = BasePostForm(self)
        if form.is_valid():
            authInfo = form.value_dict["authInfo"]
            connectHost = form.value_dict["connectHost"]
            connectPort = form.value_dict["connectPort"]
            desc = form.value_dict["desc"]
            env = form.value_dict["env"]
            name = form.value_dict["name"]
        else:
            form_error(self, form)
            return

        host_db = CmdbHost()

        code, msg = host_db.post(authInfo, connectHost, connectPort, desc, env,
                                 name)
        if not code:
            self.send_fail(msg=msg)
        else:
            # 保存成功的时候 发送消息到mq, 检测主机联通性
            if authInfo and msg:
                mq = PublishMQ()
                hostinfo = dict(id=msg, host=connectHost, port=connectPort)
                mq.send_ansible_msg(hostinfo=hostinfo,
                                    task="setup",
                                    authinfo=authInfo)
            self.send_ok(data="添加成功")
        return

    @check_request_permission()
    @coroutine
    def get(self):
        LOG.debug(self.request_body())
        form = GETBaseForm(self)
        if form.is_valid():
            pageIndex = form.value_dict["pageIndex"]
            pageSize = form.value_dict["pageSize"]
            sortBy = form.value_dict["sortBy"]
            descending = form.value_dict["descending"]
            name = form.value_dict["name"]
        else:
            form_error(self, form)
            return
        HostDB = CmdbHost()
        totalCount, get_db = HostDB.getPage(pageIndex, pageSize, descending,
                                            name)
        rows = [dbObjFormatToJson(item) for item in get_db]
        if sortBy:
            rows = sorted(rows, key=lambda x: x[sortBy], reverse=descending)
        LOG.debug(rows)
        data = dict(totalCount=totalCount, rows=rows)
        return self.send_ok(data=data)

    @check_request_permission()
    @coroutine
    def delete(self):
        FAILD_LIST = []
        req_data = self.request_body()
        LOG.debug(req_data)
        ids = req_data.get("ids", [])
        try:
            ids = json.loads(ids)
        except Exception:
            pass
        HostDB = CmdbHost()
        for item in ids:
            code, msg = HostDB.delById(item)
            if not code:
                FAILD_LIST.append(item)
        if FAILD_LIST:
            req_data = {"有成功删除的资产": FAILD_LIST}
        else:
            req_data = "删除成功"
        self.send_ok(data=req_data)
        return


@route("/cmdb/property/{}".format(uuid_re))
class UuidReHandler(MixinRequestHandler):
    """
        /xxx/xxxx/uuid 对次uuid数据的相关操作
        get: 获取UUID的基本信息
        put: 修改信息
    """
    @check_request_permission()
    @coroutine
    def get(self, id):
        HostDB = CmdbHost()
        uuid_info = HostDB.getById(id)
        uuid_info = dbObjFormatToJson(uuid_info)
        LOG.debug(uuid_info)
        self.send_ok(data=uuid_info)
        return

    @check_request_permission()
    @coroutine
    def put(self, id):
        form = PUTBaseForm(self)
        if form.is_valid():
            authInfo = form.value_dict["authInfo"]
            connectHost = form.value_dict["connectHost"]
            connectPort = form.value_dict["connectPort"]
            desc = form.value_dict["desc"]
            env = form.value_dict["env"]
            name = form.value_dict["name"]
        else:
            form_error(self, form)
            return
        HostDB = CmdbHost()
        db_status, msg = HostDB.put(authInfo, connectHost, connectPort, desc,
                                    env, name, id)
        if db_status:
            # 修改信息之后  重新检测主机联通性
            if authInfo:
                mq = PublishMQ()
                hostinfo = dict(id=id, host=connectHost, port=connectPort)
                mq.send_ansible_msg(hostinfo=hostinfo,
                                    body=dict(module="setup"),
                                    authinfo=authInfo)
            self.send_ok(data="修改成功")
        else:
            self.send_fail(msg=msg)
        return

    @check_request_permission()
    @coroutine
    def delete(self, id):
        HostDB = CmdbHost()
        code, msg = HostDB.delById(id)
        if code:
            self.send_ok(data="")
        else:
            self.send_fail(msg="")
        return


@route("/cmdb/test")
class TestHandler(MixinRequestHandler):
    """
        测试侧时候使使用
    """
    @coroutine
    def get(self):
        req_data = self.from_data()
        test_info = req_data.get("test_info", None)

        if test_info == "getadminbyid":
            id = req_data.get("id", None)
            admin_db = CmdbAdminUser()
            get_admin = admin_db.getById(id)
            return_info = dbObjFormatToJson(get_admin)
            self.send_ok(data=return_info)
            return

        if test_info == "mq_sysinfo":
            authid = "bc9670ae-f05c-4f75-8eaa-3e94999b6a7d"
            hostid = "75f2cdb3-4cf0-485c-b166-b9c48beadbf4"
            hostinfo = dict(host="192.168.2.132", port="22051", id=hostid)
            mq = SendMsgToClient(self.application.mq_server,
                                 MQ_ANSIBLE_EXCHANGE, MQ_ANSIBLE_ROUTING_KEY)
            mq.send_sysinfo(hostinfo, authid)
            self.send_ok(data="")
            return
