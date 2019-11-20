#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-20 14:59:53
@LastEditors: Youshumin
@LastEditTime: 2019-11-20 15:33:04
@Description: 
'''
from oslo.form.fields import BoolField, EmailField, IntegerField, StringField, StringListField
from oslo.form.form import Form


class SaveAdminUser(Form):
    def __init__(self, handler=None):
        self.name = StringField(required=True)
        self.sshUser = StringField(required=True)
        self.authType = IntegerField(required=True)
