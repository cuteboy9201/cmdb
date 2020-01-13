#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: YouShumin
@Date: 2019-12-26 14:53:42
@LastEditTime : 2020-01-13 02:43:39
@LastEditors  : YouShumin
@Description: 
@FilePath: /cmdb/forms/userright.py
'''
import logging

from oslo.form.fields import BoolField, EmailField, IntegerField, StringField, StringListField
from oslo.form.form import Form


class UserRightPost(Form):
    def __init__(self, handler=None):
        self.hostInfo = StringField(required=True)
        self.authUser = StringField(required=True)
        self.userInfo = StringField(required=False)
        self.roleInfo = StringField(required=False)
        self.desc = StringField(required=True)
        super(UserRightPost, self).__init__(handler=handler)


class GetUserRightInfo(Form):
    """获取授权信息 分页基本参数"""
    def __init__(self, handler=None):
        self.pageIndex = IntegerField(required=True)
        self.pageSize = IntegerField(required=True)
        self.sortBy = StringField(required=False)
        self.descending = BoolField(required=True)
        super(GetUserRightInfo, self).__init__(handler=handler)