#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
#
#   Author  :   jianfeiyun
#   E-mail  :   jianfeiyun@gmail.com
#   Date    :   2015/01/10
#   Desc    :
#

import logging, os, fcntl
import locking

class FileLock(locking.Lock):
    def __init__(self, lock_path, name):
        self.lock_path = lock_path
        lock_name = name + ".lock"
        self.lock_file = os.path.join(self.lock_path, lock_name)
        super(FileLock, self).__init__(name)

    def create_lock(self):
        try:
            self.lock_handle = open(self.lock_file, 'w')
        except Exception, ex:
            self.init_ret = False
            self.err_str = "Failed to create lock file! Exception: %s" % str(ex)
            logging.error(self.err_str)
            self.destroy_lock()

    def destroy_lock(self):
        #self.release()
        if self.lock_handle != None:
            self.lock_handle.close()
            self.lock_handle = None

    def acquire(self, blocking=True, timeout=None):
        if self.lock_handle == None:
            return None

        try:
            fcntl.flock(self.lock_handle, fcntl.LOCK_EX)
            return True
        except Exception, ex:
            self.err_str = "Acquire lock failed! Exception: %s" % str(ex)
            logging.error(self.err_str)
            return None

    def release(self):
        if self.lock_handle == None:
            return None

        try:
            fcntl.flock(self.lock_handle, fcntl.LOCK_UN)
            return True
        except Exception, err:
            logging.error("Failed acquire lock! Exception: %s", str(err))
            return None
