#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-09-16 14:50:46
# @Author  : yml_bright@163.com

import os, threading, time
import operator
from Queue import Queue
from mod.fileHandler import fileHandler
from mod.logger import printer
from mod.common import SpecialcharCount, Haship
from mod.kmeans import find_centers

class mThread(threading.Thread):
	def __init__(self, fileQueQue):
		threading.Thread.__init__(self)
		self.que = fileQueQue
		self.deamon = False

	def run(self):
		while True:
			if self.que.empty():
				break
			fileQue = self.que.get()
			metaQue = Queue()   
			x = fileHandler(fileQue, metaQue)
			x.start()
			printer.info('Start to read file.')
			fileQue.join()
			
			printer.info('Read finished, start to load.')
			x = []
			xname = []
			while not metaQue.empty():
				m = metaQue.get()
				subdomainLen = m.name.rfind('.',0,m.name.rfind('.'))
				specialCharCount = SpecialcharCount(m.name)
				distip = Haship(m.dip)
				x.append([m.datalen, subdomainLen, specialCharCount])
				xname.append(m.name)
			printer.info('Load finished, enter kmeans-mod.')
			[mu, cluster] = find_centers(x,7)
			printer.info('Sort finished, save result to file.')
			outfile = os.path.join('/kmeans',str(time.time()))
			fp = open(outfile,'a+')
			for clu in cluster:
				fp.write('Cluster %s#\n'%str(clu))
				for n in cluster[clu]:
					fp.write("%s\t%d|%d|%d\n"%(xname[n], x[n][0], x[n][1], x[n][2]))
				fp.write('\n\n\n\n\n')
			fp.close()
			printer.info('Save finished, thread exit')
			self.que.task_done()


fQue = Queue()

fileQue = Queue()
fileQue.put('2020.log', True)

fQue.put(fileQue, True)
t = mThread(fQue)
t.start()
fQue.join()
print 'count finished'
