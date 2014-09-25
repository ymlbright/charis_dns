#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-09-16 23:08:00
# @Author  : 17monip yml_bright@163.com

import os
import mmap
import struct
import socket

_unpack_V = lambda b: struct.unpack("<L", b)[0]
_unpack_N = lambda b: struct.unpack(">L", b)[0]
_unpack_C = lambda b: ord(b)

class IPv4Database(object):
    """Database for search IPv4 address.

    The 17mon dat file format in bytes::

        -----------
        | 4 bytes |                     <- offset number
        -----------------
        | 256 * 4 bytes |               <- first ip number index
        -----------------------
        | offset - 1028 bytes |         <- ip index
        -----------------------
        |    data  storage    |
        -----------------------
    """
    def __init__(self, filename=None):
        if filename is None:
            filename = os.path.join(os.path.dirname(__file__), "17monipdb.dat")
        with open(filename, 'rb') as f:
            buf = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        self._buf = buf

        self._offset = _unpack_N(buf[:4])
        self._is_closed = False

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self._buf.close()
        self._is_closed = True

    def _lookup_ipv4(self, ip):
        nip = socket.inet_aton(ip)

        # first IP number
        fip = bytearray(nip)[0]
        # 4 + (fip - 1) * 4
        fip_offset = fip * 4 + 4

        # position in the index block
        count = _unpack_V(self._buf[fip_offset:fip_offset + 4])
        pos = count * 8

        offset = pos + 1028

        data_length = 0
        data_pos = 0

        while offset < self._offset:
            endip = self._buf[offset:offset + 4]
            if nip <= endip:
                data_pos = _unpack_V(
                    self._buf[offset + 4:offset + 7] + b'\0'
                )
                data_length = _unpack_C(self._buf[offset + 7])
                break
            offset += 8

        if not data_pos:
            return None

        offset = self._offset + data_pos - 1024
        value = self._buf[offset:offset + data_length]
        return value.decode('utf-8').strip()

    def find(self, ip):
        if self._is_closed:
            raise ValueError('I/O operation on closed dat file')

        return self._lookup_ipv4(ip)

ip = IPv4Database()

def find(ip):
    # keep find for compatibility
    try:
        ip = socket.gethostbyname(ip)
    except socket.gaierror:
        return

    with IPv4Database() as db:
        return db.find(ip)
