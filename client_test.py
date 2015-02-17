#! /usr/bin/env python

import socket

host = 'localhost'
port = 9091
size = 4096

s = socket.socket()
s.connect((host, port))

string = input('> ').encode()

s.send(string)
s.close()
