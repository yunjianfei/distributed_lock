#!/usr/bin/env python2.7
#
#   Author  :   jianfeiyun
#   E-mail  :   jianfeiyun@gmail.com
#   Date    :   2015/01/10
#   Desc    :
#
from mysql_lock import MysqlLock
import logging, sys, time

def init_mysql_lock_handle():
    worker_lock_handle = MysqlLock('192.168.10.10', 3306, "test", "root", "", "lock")
    if not worker_lock_handle.init_ret:
        logging.error("Init MysqlLock : Failed to connect to mysql server!")
        return None
    return worker_lock_handle

try:
    lock = init_mysql_lock_handle()
except Exception, ex:
    print "Init mysql lock failed! Exception:" + str(ex)
    return

#none blocking
ret = lock.acquire(blocking=False)

#blocking
#ret = lock.acquire()
if ret:
    print "Get lock success! Sleep 50 secs"
    for i in range(0, 50):
        time.sleep(1)
        print str(i)

    lock.release()
else:
    print "Required lock failed! Please retry!"
