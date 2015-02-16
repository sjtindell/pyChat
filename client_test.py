#! /usr/bin/env python

import socket

host = 'localhost'
port = 5000
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

string = raw_input('> ')

s.send(string)
data = s.recv(size)
print 'response:', data
s.close()
