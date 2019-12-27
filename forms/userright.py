#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: YouShumin
@Date: 2019-12-26 14:53:42
@LastEditTime : 2019-12-26 15:09:15
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
