#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-20 11:40:07
@LastEditors: YouShumin
@LastEditTime: 2020-04-01 18:48:12
@Description: 
'''
import datetime
import logging

from configs.setting import DB_NAME
from dblib import module as ORM
from oslo.db.module import mysqlHanlder
from oslo.util import create_id, dbObjFormatToJson
from sqlalchemy import and_, asc, desc

LOG = logging.getLogger(__name__)


class MixDbObj(object):
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

    def getAllByKeyValue(self, key, value):
        item = {key: value}
        db = self.db_obj.filter_by(**item).all()
        return db

    def getAll(self):
        dbList = self.db_obj.all()
        return dbList

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
                auth_host = self.session.query(ORM.CmdbHost).filter(
                    ORM.CmdbHost.authInfo == auth.id).all()

                isactive = 0
                disactive = 0
                rank = 0
                hostnums = 0

                if auth_host:
                    hostnums = len(auth_host)
                    for item in auth_host:
                        if item.status == 1:
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
    """
        cmdb_host_auth【资产管理账号关联表】 操作
    """
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


class CmdbHost(MixDbObj):
    """ 
        IT资产表 相关操作
        post: 添加资产操作
        getPage: 获取分页资产列表
        put: 修改数据
    """
    def __init__(self, table=''):
        self.table = ORM.CmdbHost
        super(CmdbHost, self).__init__(self.table)

    def post(self, authInfo, connectHost, connectPort, desc, env, name):
        check_name = self.getDbObjByKeyValue("name", name)
        if check_name:
            return False, "资产已经存在"

        try:
            id = create_id()
            add_data = self.table(name=name,
                                  authInfo=authInfo,
                                  connectHost=connectHost,
                                  connectPort=connectPort,
                                  desc=desc,
                                  env=env,
                                  id=id,
                                  createTime=datetime.datetime.now(),
                                  updateTime=datetime.datetime.now())
            self.session.add(add_data)
            self.session.commit()
            return True, id
        except Exception as e:
            LOG.warning("{}".format(str(e)))
            self.session.rollback()
            return False, ""

    def getPage(self, pageIndex, pageSize, descending, name):

        offset_num = (pageIndex - 1) * pageSize
        db_obj = self.db_obj
        if name:
            db_obj = db_obj.filter(self.table.name == name)
        db = db_obj.all()
        totalCount = len(db)
        get_db = db_obj.limit(pageSize).offset(offset_num).all()
        return totalCount, get_db

    def put(self, authInfo, connectHost, connectPort, desc, env, name, id):
        check_id = self.getById(id)
        if not check_id:
            return False, "非法操作"
        try:
            check_id.name = name
            check_id.connectHost = connectHost
            check_id.connectPort = connectPort
            check_id.desc = desc
            check_id.authInfo = authInfo
            check_id.env = env
            check_id.updateTime = datetime.datetime.now()
            self.session.commit()
        except Exception as e:
            LOG.warning("{}".format(str(e)))
            self.session.rollback()
            return False, ""
        return True, ""


class CmdbUserRight(MixDbObj):
    """
    
    """
    def __init__(self, table=''):
        self.table = ORM.CmdbUserRight
        super(CmdbUserRight, self).__init__(table=self.table)

    def post(self, hostInfo, authUser, userInfo, roleInfo, desc):
        try:
            id = create_id()
            add_data = self.table(id=id,
                                  hostInfo=hostInfo,
                                  authUser=authUser,
                                  userInfo=userInfo,
                                  roleInfo=roleInfo,
                                  desc=desc,
                                  createTime=datetime.datetime.now(),
                                  updateTime=datetime.datetime.now())
            self.session.add(add_data)
            self.session.commit()
            return True, id
        except Exception as e:
            LOG.warning("{}".format(str(e)))
            self.session.rollback()
            return False, ""

    def getPage(self, pageIndex, pageSize, descending):
        offset_num = (pageIndex - 1) * pageSize
        db_obj = self.db_obj
        # 搜索...
        db = db_obj.all()
        totalCount = len(db)
        get_db = db_obj.limit(pageSize).offset(offset_num).all()
        return totalCount, get_db

    def getRightHost(self, roleId="", userId=""):
        db_obj = self.db_obj.all()


class CmdbSysUserAuth(MixDbObj):
    def __init__(self, table=''):
        self.table = ORM.CmdbSysUserAuth
        super(CmdbSysUserAuth, self).__init__(table=self.table)

    def check_exits(self, hostId, authUser):
        check_data = self.db_obj.filter(
            self.table.hostId == hostId,
            self.table.authUser == authUser).first()
        return check_data

    def post(self, hostId, authUser, authPass, authPriKey, authPubKey):
        check_data = self.check_exits(hostId, authUser)
        if check_data:
            return "exist", check_data.id
        id = create_id()
        try:
            add_data = self.table(id=id,
                                  hostId=hostId,
                                  authUser=authUser,
                                  authPass=authPass,
                                  authPriKey=authPriKey,
                                  authPubKey=authPubKey,
                                  createTime=datetime.datetime.now(),
                                  updateTime=datetime.datetime.now())
            self.session.add(add_data)
            self.session.commit()
            return True, id
        except Exception as e:
            LOG.error(e)
            self.session.rollback()
            return False, ""
