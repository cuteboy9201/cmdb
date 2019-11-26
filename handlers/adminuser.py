#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-19 14:34:42
@LastEditors: Youshumin
@LastEditTime: 2019-11-26 16:23:19
@Description: 
'''
import json
import logging

from oslo.form.form import form_error
from oslo.util import dbObjFormatToJson
from oslo.web.requesthandler import MixinRequestHandler
from oslo.web.route import route
from tornado.gen import coroutine

from dblib.crud import CmdbAdminUser, CmdbHostAuth
from forms.adminuser import (GetAdminUserForm, SaveAdminUserForm,
                             putAdminUserForm)
from utils.sshkey import check_ssh_key

LOG = logging.getLogger(__name__)

uuid_re = "(?P<id>[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})"


@route("/cmdb/adminuser/")
class AdminUserBaseHandler(MixinRequestHandler):
    @coroutine
    def get(self):
        '''
        @description: 获取管理账号信息,并计算当前可管理主机状态
        @param {type} 
        @return: 
        '''
        form = GetAdminUserForm(self)
        if form.is_valid():
            pageIndex = form.value_dict["pageIndex"]
            pageSize = form.value_dict["pageSize"]
            sortBy = form.value_dict["sortBy"]
            descending = form.value_dict["descending"]
            name = form.value_dict["name"]
        else:
            form_error(self, form)
            return
        AdminUserDB = CmdbAdminUser()

        totalCount, adminUserList = AdminUserDB.getAdminActice(
            pageIndex, pageSize, sortBy, descending, name)
        data = dict(totalCount=totalCount, rows=adminUserList)
        self.send_ok(data=data)
        return

    @coroutine
    def post(self):
        """ 添加host主机账号 """
        form = SaveAdminUserForm(self)
        if form.is_valid():
            name = form.value_dict["name"]
            sshUser = form.value_dict["sshUser"]
            authType = form.value_dict["authType"]
            sshPass = form.value_dict["sshPass"]
            sshKey = form.value_dict["sshKey"]
            sudoPass = form.value_dict["sudoPass"]
            desc = form.value_dict["desc"]
        else:
            form_error(self, form)
            return

        if authType == 2:
            #authType为2的时候是 密钥认证方式
            status, _ = check_ssh_key(sshKey)
            if not status:
                self.send_error(msg="密钥错误,请重新输入")
                return

        AdminUserDB = CmdbAdminUser()
        db_status, msg = AdminUserDB.post(name=name,
                                          sshUser=sshUser,
                                          authType=authType,
                                          sshPass=sshPass,
                                          sshKey=sshKey,
                                          sudoPass=sudoPass,
                                          desc=desc)
        if not db_status:
            LOG.warn("添加管理账号失败: {}".format(self.request_body()))
            self.send_error(msg=msg)
            return
        return self.send_ok(data=u"添加成功")

    @coroutine
    def put(self):
        """修改管理账号信息"""
        form = putAdminUserForm(self)
        if form.is_valid():
            id = form.value_dict["id"]
            name = form.value_dict["name"]
            sshUser = form.value_dict["sshUser"]
            authType = form.value_dict["authType"]
            sshPass = form.value_dict["sshPass"]
            sshKey = form.value_dict["sshKey"]
            sudoPass = form.value_dict["sudoPass"]
            desc = form.value_dict["desc"]
        else:
            form_error(self, form)
            return
        if authType == 2:
            # authType为2的时候是 密钥认证方式
            status, _ = check_ssh_key(sshKey)
            if not status:
                self.send_error(msg="密钥错误,请重新输入")
                return

        AdminUserDB = CmdbAdminUser()
        db_status, msg = AdminUserDB.put(id=id,
                                         name=name,
                                         sshUser=sshUser,
                                         authType=authType,
                                         sshPass=sshPass,
                                         sshKey=sshKey,
                                         sudoPass=sudoPass,
                                         desc=desc)
        if db_status:
            self.send_ok(data="修改成功")
        else:
            self.send_error(msg=msg)
        return

    @coroutine
    def delete(self):
        '''
        @description: 批量删除
        @param: {"ids": '["xxxxxxx", "xxxxxxxxxxxxxx"]'}
        @return: 
        '''
        FAILD_LIST = []
        req_data = self.request_body()
        LOG.debug(req_data)
        ids = req_data.get("ids", [])
        try:
            ids = json.loads(ids)
        except Exception:
            pass
        AuthHostMap = CmdbHostAuth()
        for item in ids:
            check_auth_map = AuthHostMap.checkMapByauthId(item)
            if check_auth_map:
                FAILD_LIST.append(item)
            else:
                AuthDb = CmdbAdminUser()
                code, msg = AuthDb.delById(item)
        if FAILD_LIST:
            reps_data = {"有绑定资产账号未删除": FAILD_LIST}
        else:
            reps_data = "删除成功"
        self.send_ok(data=reps_data)
        return


@route("/cmdb/adminuser/{}".format(uuid_re))
class uuidRequestHandler(MixinRequestHandler):
    @coroutine
    def get(self, id):

        AdminUserDB = CmdbAdminUser()
        uuidInfoDb = AdminUserDB.getById(id)
        uuidData = dbObjFormatToJson(uuidInfoDb)
        LOG.debug(uuidData)
        return self.send_ok(data=uuidData)

    @coroutine
    def delete(self, id):
        AuthHostMap = CmdbHostAuth()
        check_auth_map = AuthHostMap.checkMapByauthId(id)
        if check_auth_map:
            self.send_error(msg="此账号有绑定资产信息,请先解除绑定")
            return
        AuthDb = CmdbAdminUser()
        code, msg = AuthDb.delById(id)
        if code:
            self.send_ok(data="")
        else:
            self.send_error(msg=msg)
        return
