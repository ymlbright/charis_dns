#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-09-18 18:10:49
# @Author  : yml_bright@163.com

import os, threading, time
from Queue import Queue
from mod.logger import printer
from mod.dbHandler import dbHandler
from mod.kmeans import find_centers

class mThread(threading.Thread):
	def __init__(self, fileQue):
		threading.Thread.__init__(self)
		self.que = fileQue
		self.deamon = True

	def run(self):
		while True:
			if self.que.qsize() <= 0 :
				printer.info('Finished')
				break
			x = self.que.get()
			#db.register('cmeans')
			#db.init('cmeans', 'name text, count inteager, p inteager')
			printer.info('Start to load file: %s'%x)
			f = open(x,'r')
			l = f.readline()
			cmeans = []
			cname = []
			clen = 0
			while l:
				#printer.info(l)
				d = l.split('\t')
				cmeans.append([int(d[1])])
				cname.append(d[0])
				clen += 1
				l = f.readline()
			f.close()
			printer.info('Load finished, enter k-means')
			[mu, cluster] = find_centers(cmeans,10)
			printer.info('K-means finished, start to save result')
			#cur = db.get(model).cursor()
			f = open(x+'.txt','w')
			for clu in cluster:
				l = len(cluster[clu])
				for c in cluster[clu]:
					f.write('%s\t%f\n'%(cname[c],float(l*cmeans[c][0])/float(clen)))
			f.close()
			self.que.task_done()
#db = dbHandler()
fileQue = Queue()
for d in os.listdir('/count/'):
	p = os.path.join('/count/',d)
	if not os.path.isfile(p):
		continue
	if os.path.splitext(p)[1]=='.txt':
		continue
	fileQue.put(p, True)
	printer.info('Put %s'%p)


for i in range(20):
	th = mThread(fileQue)
	th.start()
	printer.info('Starting thread...')
fileQue.join()

print 'Count finished'


			

