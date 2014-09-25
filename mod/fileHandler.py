#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-09-12 08:49:22
# @Author  : yml_bright@163.com

import os, threading
from logger import logger
from metaDNS import metaDNS
from Queue import Queue

class fileHandler(threading.Thread):
	def __init__(self, fileQue, metaQue):
		threading.Thread.__init__(self)
		self.daemon = False
		self.fileque = fileQue
		self.metaque = metaQue

	def run(self):
		while True:
			if self.fileque.empty():
				break
			fp = self.open_file(self.fileque.get())
			self.load(fp)
			self.fileque.task_done()

	def open_file(self, file):
		if os.path.isfile(file):
			try:
				return open(file, 'r')
			except IOError as e:
				logger.error('IOError(%d): %s'%(e.errno, e.strerror))
		else:
			logger.warning('No such file \'%s\'.'%file)

	def load(self, fp):
		if fp:
			frame = fp.readline()
			data = fp.readline()
			fp.readline()
			while frame:
				x = metaDNS(frame, data)
				self.metaque.put(x, True)
				frame = fp.readline()
				data = fp.readline()
				fp.readline()
		else:
			logger.warning('Read file without vaild handler.')

if __name__ == '__main__':
	fileQue = Queue()
	fileQue.put('0122.log', True)
	metaQue = Queue()
	x = fileHandler(fileQue, metaQue)
	x.start()
	print 'start finished'
	fileQue.join()
	print metaQue.get()
