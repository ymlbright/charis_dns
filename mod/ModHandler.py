#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-12 13:06:31
# @Author  : yml_bright@163.com

import os


class ReportObject(object):
	def __init__(self, type, DomainName, SIP, DIP):
		pass

class ModHandler(object):
	def __init__(self, metaQueue, reportQueue):
		pass

	def report(self):
		reportQueue.put(ReportObject)