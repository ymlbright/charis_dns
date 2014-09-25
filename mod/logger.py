#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-09-11 23:26:18
# @Author  : yml_bright@163.com

import sys
import logging

logger = logging.getLogger("CHAIRSDNS")
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s', \
			'%Y-%m-%d %H:%M:%S')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)

printer = logging.getLogger('MyPrinter')
formatter = logging.Formatter('[%(asctime)s][%(thread)d] %(message)s', '%H:%M:%S')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
printer.setLevel(logging.INFO)
printer.addHandler(stream_handler)