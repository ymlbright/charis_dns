#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-09-16 15:44:29
# @Author  : yml_bright@163.com

from IPData.IP import ip

def SpecialcharCount(s):
	n = 0
	for c in s:
		if not 0x2d<=c<=0x39 and 0x41<=c<=0x5a and 0x61<=c<=0x7a:
			# not in '-' '.' '/' 0'~'9' 'A'~'Z' 'a'~'z'
			n = n + 1
	return n

def Haship(s):
	a = ip.find(s)
	#print a.encode('utf-8')
	h = 0
	for i in range(1, len(a)+1):
		h += i*ord(a[i-1])
	return h%65537

if __name__ == '__main__':
	print Haship('79.11.12.1')