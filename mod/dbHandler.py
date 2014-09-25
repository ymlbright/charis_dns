#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-09-12 12:57:35
# @Author  : yml_bright@163.com

import sqlite3, time
import pickle
from logger import logger

class dbHandler(object):
	def __init__(self):
		self.conn = {}
		self.lock = {}

	def register(self, model, file=':memory:'):
		try:
			self.conn[model]
			logger.warning('ModelError: Model already exist.')
		except KeyError:
			self.conn[model] = sqlite3.connect(file)
			self.lock[model] = False

	def load(self, model):
		try:
			self.conn[model]
			logger.warning('ModelError: Model already exist.')
		except KeyError:
			filePath = model + '.pkl'
			if os.path.isfile(filePath):
				try:
					f = open(filePath, 'r')
					self.conn[model] = pickle.load(f)
					f.close()
				except IOError as e:
					logger.error('IOError(%d): %s'%(e.errno, e.strerror))
			else:
				logger.warning('No such file \'%s\'.'%file) 

	def save(self, model):
		filePath = model + '.pkl'
		with open(filePath,'w') as f:
			pickle.dump(self.conn[model],f)

	def get(self, model):
		try:
			while self.lock[model]:
				time.sleep(0.5)
			return self.conn[model]
		except KeyError:
			logger.error('KeyError: Error model name.')

	def init(self, model, colume):
		try:
			cur = self.conn[model].cursor()
			cur.execute('CREATE TABLE item(%s)'%colume)
			self.conn[model].commit()
		except KeyError:
			logger.error('KeyError: Error model name.')

	def __del__(self):
		for model in self.conn:
			if self.conn[model]:
				self.conn[model].close()

	def __getattribute__(self, key):
		if key in ['conn', 'lock', 'get', 'init', 'register']:
			return object.__getattribute__(self, key)
		try:
			while self.lock[key]:
				time.sleep(0.5)
			return self.conn[key]
		except AttributeError:
			return object.__getattribute__(self, key)
		except KeyError:
			logger.error('KeyError: Error model name.')