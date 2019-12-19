#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-20 17:48:48
@LastEditors  : Please set LastEditors
@LastEditTime : 2019-12-18 15:53:54
@Description:
'''
import rsa
from configs.setting import PATH_APP_ROOT
from oslo.util import create_id
import logging
import os
LOG = logging.getLogger(__name__)


def check_ssh_key(sshkey):
    try:
        pri_key = rsa.PrivateKey.load_pkcs1(sshkey)
        pri_file = pri_key.save_pkcs1()
        return True, pri_file
    except Exception:
        LOG.warning("check_ssh_key error: {}".format(str(sshkey)))
        return False, ""


# def make_auth_file(key):
#     tmp_key_file = "%s/.%s" % (PATH_APP_ROOT, create_id())
#     with open(tmp_key_file, "w+") as tkf:
#         status, msg = check_ssh_key(key)
#         if status:
#             tkf.write(msg)
#             os.system("chmod 600 %s" % tmp_key_file)
#             return True, tmp_key_file
#         else:
#             return False, ""
