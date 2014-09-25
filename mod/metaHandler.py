#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-09-11 17:38:33
# @Author  : yml_bright@163.com

import os, threading, time

from logger import logger
from Queue import Queue

class metaHandler(threading.Thread):
	def __init__(self, metaQue):
		threading.Thread.__init__(self)
		threading.daemon = False
		self.metaque = metaQue

	def run(self):
		while True:
			if self.que.empty():
				time.sleep(2)
				continue
			x = self.que.get()
			....
			

