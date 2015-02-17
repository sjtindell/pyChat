import select
import socket
import sys


class ChatClient(object):

    def __init__(self, host='localhost', port=51515, buffer=4096, user='Me'):
        self.host = host
       	self.port = port
        self.buffer = buffer
        self.socket = None
        self.user = user

    def start(self):
        self.socket = socket.socket()
        self.socket.settimeout(2)
		
        try:
            self.socket.connect((self.host, self.port))
            print('Connected to remote host.')
            sys.stdout.write('[' + self.user + '] ')
            sys.stdout.flush()
        except Exception as e:
            print('Connection failed:', e)
            sys.exit(0)

        while True:
            socket_list = [sys.stdin, self.socket]
            to_read, to_write, errors = select.select(socket_list, [], [])

            for connection in to_read:
                if connection == self.socket:
                    data = connection.recv(self.buffer)
                    if not data:
                        print('\n no server connection')
                        sys.exit(0)
                    else:
                        data = data.decode()
                        sys.stdout.write(data)
                        sys.stdout.write('[' + self.user + '] ')
                        sys.stdout.flush()
                else:
                    msg = sys.stdin.readline()
                    msg = msg.encode('utf-8')
                    self.socket.send(msg)
                    sys.stdout.write('[' + self.user + '] ')
                    sys.stdout.flush()



