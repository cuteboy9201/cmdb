#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-19 14:28:19
@LastEditors  : Please set LastEditors
@LastEditTime : 2019-12-19 15:00:16
@Description: 
'''
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class CmdbAuth(Base):
    """
        管理账户表
    """
    __tablename__ = 'cmdb_auth'

    id = Column(String(40), primary_key=True)
    name = Column(String(40), nullable=False)
    sshUser = Column(String(40), nullable=False)
    sshPass = Column(String(64))
    sudoPass = Column(String(64))
    authType = Column(TINYINT(1))
    sshKey = Column(String(2048))
    desc = Column(String(64), nullable=False)


class CmdbHost(Base):
    """
        IT资产表
    """
    __tablename__ = 'cmdb_host'

    id = Column(String(40), primary_key=True)
    name = Column(String(40), nullable=False)
    authInfo = Column(String(40), nullable=True)
    connectHost = Column(String(40))
    connectPort = Column(INTEGER(5), nullable=False)
    env = Column(String(40))
    hostname = Column(String(64))
    address = Column(String(64))
    sysinfo = Column(String(64))
    hdinfo = Column(String(64))
    status = Column(TINYINT(1))
    adminuser = Column(String(64))
    createTime = Column(DateTime)
    updateTime = Column(DateTime)
    desc = Column(String(64), nullable=False)


class CmdbHostAuth(Base):
    """
        绑定资产管理账号
    """
    __tablename__ = 'cmdb_host_auth'

    id = Column(String(40), primary_key=True)
    hostId = Column(ForeignKey("cmdb_host.id"), index=True)
    authId = Column(ForeignKey("cmdb_auth.id"), index=True)
    cmdb_auth = relationship("CmdbAuth", backref="auth_cmdb")
    cmdb_host = relationship("CmdbHost", backref="host_cmdb")


if __name__ == "__main__":
    from app import DB
    DB().db_init()
    from configs.setting import DB_NAME
    from oslo.db.module import mysqlHanlder
    engin = mysqlHanlder().get_engin(DB_NAME)
    import sys

    num = len(sys.argv)
    if num != 2:
        sys.exit(1)
    if sys.argv[1] == "create":
        metadata.create_all(engin)
    elif sys.argv[1] == "drop":
        metadata.drop_all(engin)
