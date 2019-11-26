#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-20 11:40:07
@LastEditors: Youshumin
@LastEditTime: 2019-11-26 10:14:54
@Description: 
'''
import datetime
import logging

from oslo.db.module import mysqlHanlder
from oslo.util import create_id, dbObjFormatToJson
from sqlalchemy import and_, desc, asc

from configs.setting import DB_NAME
from dblib import module as ORM

LOG = logging.getLogger(__name__)


class MixDbObj:
    def __init__(self, table=""):
        self.table = table
        self.session = mysqlHanlder().get_session(db_name=DB_NAME)
        self.db_obj = self.session.query(self.table)

    def getById(self, id):
        item = self.db_obj.filter(self.table.id == id).first()
        return item

    def delById(self, id):
        del_data = self.getById(id)
        if del_data:
            try:
                self.session.delete(del_data)
                self.session.commit()
                return True, "删除成功"
            except Exception:
                LOG.warn("delete table {} by id {} not iexit".format(
                    self.table, id))
                self.session.rollback()
                return False, "删除失败"
        return False, "删除数据不存在"

    def getDbObjByKeyValue(self, key, value):
        item = {key: value}
        db = self.db_obj.filter_by(**item).first()
        return db

    def __del__(self):
        self.session.close()


class CmdbAdminUser(MixDbObj):
    def __init__(self, tabel=None):
        self.table = ORM.CmdbAuth
        super(CmdbAdminUser, self).__init__(self.table)

    def post(self, name, sshUser, authType, sshPass, sshKey, sudoPass, desc):
        check_name = self.getDbObjByKeyValue("name", name)
        if check_name:
            return False, "账号已经存在"
        try:
            id = create_id()
            add_data = self.table(name=name,
                                  sshUser=sshUser,
                                  sshPass=sshPass,
                                  sudoPass=sudoPass,
                                  sshKey=sshKey,
                                  authType=authType,
                                  desc=desc,
                                  id=id)
            self.session.add(add_data)
            self.session.commit()
            return True, id
        except Exception as e:
            LOG.error("{}".format(str(e)))
            self.session.rollback()
            return False, ""

    def put(self, id, name, sshUser, authType, sshPass, sshKey, sudoPass,
            desc):
        check_id = self.getById(id)
        if not check_id:
            return False, "非法操作"
        try:
            check_id.name = name
            check_id.sshUser = sshUser
            check_id.authType = authType
            check_id.sshPass = sshPass
            check_id.sshKey = sshKey
            check_id.sudoPass = sudoPass
            check_id.desc = desc
            self.session.commit()
        except Exception as e:
            LOG.error("{}".format(str(e)))
            self.session.rollback()
            return False, ""
        return True, ""

    def getAdminActice(self, pageIndex, pageSize, sortBy, descending, name):
        reps_list = []

        offset_num = (pageIndex - 1) * pageSize
        db_obj = self.db_obj
        if name:
            db_obj = db_obj.filter(self.table.name == name)
        db = db_obj.all()
        totalCount = len(db)
        get_db = db_obj.limit(pageSize).offset(offset_num).all()

        if get_db:
            for auth in get_db:
                auth_host = self.session.query(ORM.CmdbHostAuth).filter(
                    ORM.CmdbHostAuth.authId == auth.id).all()

                isactive = 0
                disactive = 0
                rank = 0
                hostnums = 0

                if auth_host:
                    hostnums = len(auth_host)

                    for item in auth_host:
                        if item.cmdb_host.status == 1:
                            isactive += 1
                        else:
                            disactive += 1
                    rank = round(isactive / hostnums) * 100
                reps_list.append(
                    dict(id=auth.id,
                         name=auth.name,
                         sshUser=auth.sshUser,
                         nums=hostnums,
                         activeNums=isactive,
                         disActiveNums=disactive,
                         rank=rank,
                         desc=auth.desc))
        if sortBy:
            reps_list = sorted(reps_list,
                               key=lambda x: x[sortBy],
                               reverse=descending)
        return totalCount, reps_list


class CmdbHostAuth(MixDbObj):
    def __init__(self, table=''):
        self.table = ORM.CmdbHostAuth
        super(CmdbHostAuth, self).__init__(self.table)

    def checkMapByauthId(self, authId):
        DB = self.db_obj.filter(self.table.authId == authId).first()
        return DB

    def checkMapByHostId(self, hostId):
        DB = self.db_obj.filter(self.table.hostId == hostId).first()
        return DB

    def getListDataByHostId(self, hostId):
        DB = self.db_obj.filter(self.table.hostId == hostId).all()
        return DB

    def getListDataByAuthId(self, authId):
        DB = self.db_obj.filter(self.table.authId == authId).all()
        return DB
