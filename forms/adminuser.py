#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-20 14:59:53
@LastEditors: Youshumin
@LastEditTime: 2019-11-26 10:10:37
@Description: 
'''
from oslo.form.fields import BoolField, EmailField, IntegerField, StringField, StringListField
from oslo.form.form import Form


class SaveAdminUserForm(Form):
    """添加管理账号 参数基本验证"""
    def __init__(self, handler=None):
        self.name = StringField(required=True)
        self.sshUser = StringField(required=True)
        self.authType = IntegerField(required=True)
        self.sshPass = StringField(required=False, key=True)
        self.sshKey = StringField(required=False)
        self.sudoPass = StringField(required=False)
        self.desc = StringField(required=True)
        super(SaveAdminUserForm, self).__init__(handler=handler)


class GetAdminUserForm(Form):
    """获取管理账号 分页基本参数"""
    def __init__(self, handler=None):
        self.pageIndex = IntegerField(required=True)
        self.pageSize = IntegerField(required=True)
        self.sortBy = StringField(required=False)
        self.descending = BoolField(required=True)
        self.name = StringField(required=False)
        super(GetAdminUserForm, self).__init__(handler=handler)


class putAdminUserForm(Form):
    """ 修改管理账号信息 """
    def __init__(self, handler=None):
        self.id = StringField(required=True)
        self.name = StringField(required=True)
        self.sshUser = StringField(required=True)
        self.authType = IntegerField(required=True)
        self.sshPass = StringField(required=False, key=True)
        self.sshKey = StringField(required=False)
        self.sudoPass = StringField(required=False)
        self.desc = StringField(required=True)
        super(putAdminUserForm, self).__init__(handler=handler)