#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
#
#   Author  :   jianfeiyun
#   E-mail  :   jianfeiyun@gmail.com
#   Date    :   2015/01/10
#   Desc    :
#

import logging, os, time
from zk_lock import ZooKeeperLock

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    zookeeper_hosts = "192.168.10.10:2181"
    lock_name = "test"

    lock = ZooKeeperLock(zookeeper_hosts, "myid is 1", lock_name, logger=logger)
	#none blocking
    ret = lock.acquire(False)
	#blocking
	#ret = lock.acquire()
    if not ret:
        logging.info("Can't get lock! Ret: %s", ret)
        return

    logging.info("Get lock! Do something! Sleep 10 secs!")
    for i in range(1, 11):
        time.sleep(1)
        print str(i)

    lock.release()

if __name__ == "__main__":
    try:
        main()
    except Exception, ex:
        print "Ocurred Exception: %s" % str(ex)
        quit()

