#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
#
#   Author  :   jianfeiyun
#   E-mail  :   jianfeiyun@gmail.com
#   Date    :   2015/01/10
#   Desc    :
#

import logging
import locking
import torndb

class MysqlLock(locking.Lock):
    def __init__(self, db_host, db_port, db_name, db_user, db_pass, lock_name):
        self.db_handle = None
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass
        super(MysqlLock, self).__init__(lock_name)

    def _execute(self, sql):
        if self.db_handle == None:
            return None

        try:
            ret = self.db_handle.get(sql)
            return ret
        except Exception, ex:
            self.err_str = "Execute sql \"%s\" failed! Exception: %s" % (sql, str(ex))
            logging.error(self.err_str)
            return None

    def create_lock(self):
        mysql_host = self.db_host + ":" + str(self.db_port)
        try:
            self.db_handle = torndb.Connection(
                host=mysql_host, database=self.db_name,
                user=self.db_user, password=self.db_pass
            )
        except Exception, ex:
            self.init_ret = False
            self.err_str = "Failed to connect to Mysql, Exception: %s" % str(ex)
            logging.error(self.err_str)

    def destroy_lock(self):
        if self.db_handle != None:
            self.db_handle.close()
            self.db_handle = None

    def _acquire(self, timeout):
        sql = "SELECT GET_LOCK('%s', %s) as lk" % (self.name, timeout)
        ret = self._execute(sql)

        if ret == None:
            return None

        if ret.lk == 0:
            logging.debug("Another client has previously locked '%s'.", self.name)
            return False
        elif ret.lk == 1:
            logging.debug("The lock '%s' was obtained successfully.", self.name)
            return True
        else:
            logging.error("Error occurred!")
            return None

    def acquire(self, blocking=True, timeout=None):
        _timeout = timeout
        if_retry = False

        if blocking is False and timeout == None:
            _timeout = 0

        if blocking and timeout == None:
            _timeout = 30
            if_retry = True

        if if_retry is False:
            return self._acquire(_timeout)

        while blocking and if_retry:
            ret = self._acquire(_timeout)
            if ret == False:
                continue
            return ret

    def release(self):
        sql = "SELECT RELEASE_LOCK('%s') as lk" % (self.name)
        ret = self._execute(sql)

        if ret == None:
            return None

        if ret.lk == 0:
            logging.debug("The lock '%s' is not released(the lock was not established by this thread).", self.name)
            return False
        elif ret.lk == 1:
            logging.debug("The lock '%s' was released.", self.name)
            return True
        else:
            logging.error("The lock '%s' did not exist.", self.name)
            return None
