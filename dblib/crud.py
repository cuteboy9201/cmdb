#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-20 11:40:07
@LastEditors: Youshumin
@LastEditTime: 2019-11-20 11:48:22
@Description: 
'''
import datetime
import logging

from oslo.db.module import mysqlHandler
from oslo.util import create_id, dbObjFormatToJson
from sqlalchemy import and_, desc, asc

from configs.setting import DB_NAME
from dblib import models as ORM

LOG = logging.getLogger(__name__)


class MixDbObj(object):
    def __init__(self, table=""):
        self.table = table
        self.session = mysqlHandler.get_session(DB_NAME)
        self.db_obj = self.session.query(self.table)

    def getById(self, id):
        item = self.db_obj.filter(self.table.id == id).first()
        return True, item

    def delById(self, id):
        del_data = self.getById(id)
        if del_data:
            try:
                self.session.delete(del_data)
                self.session.commit()
                return True, "删除成功"
            except Exception as e:
                LOG.warn("delete table {} by id {} not iexit".format(
                    self.table, id))
                self.session.rollback()
                return False, "删除失败"
        return False, "删除数据不存在"

    def __del__(self):
        self.session.close()