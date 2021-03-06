#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-09-12 14:03:26
# @Author  : yml_bright@163.com

import os, threading, time
import operator
from Queue import Queue
from mod.fileHandler import fileHandler
from mod.logger import printer

count = {}
mutex = threading.Lock()

class mThread(threading.Thread):
	def __init__(self, metaQue):
		threading.Thread.__init__(self)
		self.que = metaQue
		self.deamon = False

	def run(self):
		global count, mutex
		while True:
			if self.que.empty():
				break
			x = self.que.get()
			mutex.acquire()
			try:
				count[x.name]
				count[x.name] += 1
			except KeyError:
				count[x.name] = 1
			mutex.release()
			self.que.task_done()

for d in os.listdir('m20130301'):
	fileQue = Queue()
	p = os.path.join('m20130301',d)
	printer.info('Load file: %s'%p)
	if not os.path.isfile(p):
		continue
	fileQue.put(p, True)
	metaQue = Queue()
	x = fileHandler(fileQue, metaQue)
	x.start()
	fileQue.join()
	printer.info('Load finished, start to count.')

	th = [ mThread(metaQue) for i in range(3)]
	for t in th:
		t.start()
	metaQue.join()
	printer.info('Count finished, start to save.')

	if count:
		result = sorted(count.iteritems(), key=operator.itemgetter(1))
		of = os.path.join('m20130301',d)
		f = open(of,'a+')
		for x in result:
			f.write('%s\t%d\n'%(x[0], x[1]))
		f.close()
	printer.info('Save finished.')
print 'Count finished'
