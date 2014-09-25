#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-09-11 17:40:37
# @Author  : yml_bright@163.com

from logger import logger

class metaDNS(object):
	def __init__(self, frame, data):
		if frame and data:
			try:
				self.frame_spliter(frame)
				self.data_spliter(data)
			except IndexError:
				logger.warning('IndexError: Error parms passed in.\n%s\n%s'%(frame,data))
		else:
			logger.warning('ParameterError: NULL parm(s) passed in.')

	def frame_spliter(self, frame):
		dict = {}
		f = frame.split(' |')
		tag = f[0].split(' ')
		dict['aid'] = int(tag[0])
		dict['index'] = int(tag[2])
		dict['timestamp'] = tag[3] +'.'+ tag[4]
		dict['sip'] = f[1][6:]
		dict['dip'] = f[2][7:]
		dict['sport'] = int(f[3][9:])
		dict['dport'] = int(f[4][9:])
		dict['proto'] = int(f[5][9:])
		dict['datalen'] = int(f[6][11:])
		self.parser(dict)

	def data_spliter(self, data):
		dict = {}
		f = data.split(' | ')
		dict['name'] = f[0]
		dict['addr'] = f[1]
		dict['type'] = int(f[2])
		dict['ttl'] = int(f[3])
		self.parser(dict)

	def parser(self, dict):
		for key,value in dict.items():
			object.__setattr__(self, key, value)

	def __getattribute__(self, key):
		try:
			return object.__getattribute__(self, key)
		except AttributeError:
			logger.warning('AttributeError: No such key \'%s\''%key)

if __name__ == '__main__':
	s = '16909060 0 40467752 1360642857 142709 APPCLASS : 3 |SIP : 219.219.159.58 | DIP : 202.119.80.11 | SPORT : 53 | DPORT : 23473 | Proto : 17 | Datalen : 76 | \nqup.qh-lb.com | 101.4.60.85 | 1 | 36'
	d = s.split('\n')
	x = metaDNS(d[0],d[1])
	print x.asd, x.aid, x.index, x.timestamp, x.sip, x.dip, x.sport, x.dport, x.proto, x.datalen, x.name, x.addr, x.type, x.ttl

