#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-19 14:28:19
@LastEditors: Youshumin
@LastEditTime: 2019-11-20 11:37:10
@Description: 
'''
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.mssql import INTEGER, TINYINT
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
    sshkey = Column(String(512))
    desc = Column(String(64), nullable=False)


class CmdbHost(Base):
    """
        IT资产表
    """
    __tablename__ = 'cmdb_host'

    id = Column(String(40), primary_key=True)
    name = Column(String(40), nullalbe=False)
    connectHost = Column(String(40))
    connectPort = Column(INTEGER(16))
    env = Column(String(40))
    hostname = Column(String(64))
    address = Column(String(64))
    sysinfo = Column(String(64))
    hdinfo = Column(String(64))
    status = Column(TINYINT(1))
    adminuser = Column(String(64))
    createTime = Column(DateTime)
    upadteTime = Column(DateTime)
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