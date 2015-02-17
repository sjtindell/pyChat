#! /usr/bin/env python

import socket

host = ''
port = 9091
backlog = 5
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(backlog)

while True:
    client, address = s.accept()
    data = client.recv(size)
    data.decode('utf-8')
    print('received data:', data)
    client.close()
