import select
import socket
import sys


class ChatClient(object):

    def __init__(self, host='localhost', port=9091, buffer=4096):
        self.host = host
        self.port = port
        self.buffer = buffer

    def start(self):
        s = socket.socket()
        s.settimeout(2)

        try:
            s.connect((self.host, self.port))
            print('Connected to remote host.')
            sys.stdout.write('[Me] ')
            sys.stdout.flush()
        except s.error as e:
            print('Connection failed:', e)
            sys.exit(0)

        while True:
            socket_list = [sys.stdin, s]
            to_read, to_write, errors = select.select(socket_list, [], [])

            for connection in to_read:
                if connection == s:
                    data = connection.recv(self.buffer)
                    if not data:
                        print('\n no server connection')
                        sys.exit(0)
                    else:
                        sys.stdout.write(data)
                        sys.stdout.write('[Me ')
                        sys.stdout.flush()
                else:
                    msg = sys.stdin.readline()
                    msg = msg.encode('utf-8', 'strict')
                    s.send(msg)
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()

