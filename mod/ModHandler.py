#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-12 13:06:31
# @Author  : yml_bright@163.com

import os, threading

class ReportObject(object):
    def __init__(self, Type, DomainName, SIP, DIP, Timestamp, Optional):
        self.Type = Type
        self.DomainName = DomainName
        self.SIP = SIP
        self.DIP = DIP
        self.Timestamp = Timestamp
        self.Optional = Optional

class ModHandler(threading.Thread):
    def __init__(self, metaQueue, reportQueue):
        threading.Thread.__init__(self)
        self.daemon = False
        self.metaQueue = metaQueue
        self.reportQueue = reportQueue

    def get(self):
        if self.metaQueue.qsize() <=0:
            return None
        return self.metaQueue.get()

    def report(self, Type, DomainName, SIP, DIP, Timestamp, Optional=None):
        self.reportQueue.put(ReportObject(Type, DomainName, SIP, DIP, Timestamp, Optional))