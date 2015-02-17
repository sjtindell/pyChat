import select
import socket
import sys


class ChatServer(object):

    # buffer defines size needed to receive data
    # backlog defines max connections
    def __init__(self, port=9091, buffer=4096, backlog=5):

        self.host = ''
        self.port = port
        self.socket_list = []
        self.buffer = buffer
        self.backlog = backlog
        self.server_socket = None

    def start(self):
        s = socket.socket()                                                 # AF_INET and SOCK_STREAM are socket defaults
        s.bind((self.host, self.port))
        s.listen(self.backlog)

        self.socket_list.append(s)                                          # ?
        self.server_socket = s
        print('chat server started on port', self.port)

    def broadcast(self, peer, text):
        for port in self.socket_list:
            if port not in (self.server_socket, peer):
                try:
                    port.send(text)
                except port.error as e:
                    print('error:', e)
                    port.close()
                    self.socket_list.remove(port)

    # def client_handler(self):
    #     s = self.server_socket
    #     while True:
    #         client, address = s.accept()
    #         data = client.recv(self.buffer)
    #         data.decode('utf-8')
    #         print('received data: ', data)
    #         client.close()

    def client_handler(self):
        s = self.server_socket

        while True:
            to_read, to_write, errors = select.select(self.socket_list, [], [], 0)  # 0 timeout, poll never block
            for connection in to_read:
                if connection == s:
                    client, address = s.accept()
                    self.socket_list.append(client)
                    print(address, 'connected')
                else:
                    data = connection.recv(self.buffer)
                    if data:
                        self.broadcast('\r' + '[' + str(connection.getpeername()) + ']', data)
                    else:
                        self.socket_list.remove(connection)

    def stop(self):
        pass



