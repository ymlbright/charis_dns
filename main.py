#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-09-12 09:39:45
# @Author  : yml_bright@163.com

from mod.fileHandler import fileHandler
from mod.dbHandler import dbHandler
from mod.kmeans import find_centers
from Queue import Queue

fileQue = Queue()
fileQue.put('0122.log', True)
metaQue = Queue()
x = fileHandler(fileQue, metaQue)
x.start()
fileQue.join()
print 'load finished'

dbset = dbHandler()
dbset.register('test','0122.db')
dbset.init('test')
db = dbset.test
cur = db.cursor()
for i in range(metaQue.qsize()):
	item = metaQue.get()
	print 'add',item.index
	cur.execute('INSERT INTO item VALUES (?,?,?,?,?,?,?,?,?,?)',
		(item.index, item.timestamp, item.name, item.sip, item.sport,
			item.dip, item.dport, item.datalen, item.addr, item.ttl))
	db.commit()

