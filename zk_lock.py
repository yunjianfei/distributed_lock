#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
#
#   Author  :   jianfeiyun
#   E-mail  :   jianfeiyun@gmail.com
#   Date    :   2015/01/10
#   Desc    :
#

import logging, os
import locking
from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.recipe.lock import Lock

class ZooKeeperLock(locking.Lock):
    def __init__(self, hosts, id_str, name, logger=None, timeout=1):
        self.hosts = hosts
        self.id_str = id_str
        self.zk_client = None

        self.timeout = timeout
        self.logger = logger
        super(ZooKeeperLock, self).__init__(name)

    def create_lock(self):
        try:
            self.zk_client = KazooClient(hosts=self.hosts, logger=self.logger, timeout=self.timeout)
            self.zk_client.start(timeout=self.timeout)
        except Exception, ex:
            self.init_ret = False
            self.err_str = "Create KazooClient failed! Exception: %s" % str(ex)
            logging.error(self.err_str)
            return

        try:
            lock_path = os.path.join("/", "locks", self.name)
            self.lock_handle = Lock(self.zk_client, lock_path)
        except Exception, ex:
            self.init_ret = False
            self.err_str = "Create lock failed! Exception: %s" % str(ex)
            logging.error(self.err_str)
            return

    def destroy_lock(self):
        #self.release()

        if self.zk_client != None:
            self.zk_client.stop()
            self.zk_client = None

    def acquire(self, blocking=True, timeout=None):
        if self.lock_handle == None:
            return None

        try:
            return self.lock_handle.acquire(blocking=blocking, timeout=timeout)
        except Exception, ex:
            self.err_str = "Acquire lock failed! Exception: %s" % str(ex)
            logging.error(self.err_str)
            return None

    def release(self):
        if self.lock_handle == None:
            return None
        return self.lock_handle.release()
