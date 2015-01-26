#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
#
#   Author  :   jianfeiyun
#   E-mail  :   jianfeiyun@gmail.com
#   Date    :   2015/01/10
#   Desc    :
#

import abc

class Lock(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name=None):
        self.name = name
        self.lock_handle = None

        self.init_ret = True
        self.err_str = None

        self.create_lock()

    def __del__(self):
        self.destroy_lock()

    @abc.abstractmethod
    def create_lock(self):
        """Attempts to create the lock handle
        if success created, set lock_handle not none
        :returns: None
        """

    @abc.abstractmethod
    def destroy_lock(self):
        """Attempts to destroy the lock handle
        :returns: None
        """

    @abc.abstractmethod
    def release(self):
        """Attempts to release the lock, returns true if released.
        The behavior of releasing a lock which was not acquired in the first
        place is undefined (it can range from harmless to releasing some other
        users lock)..
        :returns: returns true if released (false if not)
        :rtype: bool
        """

    @abc.abstractmethod
    def acquire(self, blocking=True, timeout=None):
        """Attempts to acquire the lock.
        :param blocking: If True, blocks until the lock is acquired. If False,
                         returns right away. Otherwise, the value is used as a
                         timeout value and the call returns maximum after this
                         number of seonds.
        :returns: returns true if acquired (false if not)
        :rtype: bool
        """
