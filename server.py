import select
import socket
import sys


class ChatServer(object):

    def __init__(self, port=51515, buffer=4096, backlog=5):

        self.host = '0.0.0.0'
        self.port = port
        self.socket_list = []
        self.buffer = buffer
        self.backlog = backlog
        self.server_socket = None
        self.unames = {}
        
        self.start()
        self.client_handler()

    def start(self):
        s = socket.socket()                                               
        s.bind((self.host, self.port))
        s.listen(self.backlog)

        self.socket_list.append(s)                                      
        self.server_socket = s
        print('chat server started on port', self.port)


    # def client_handler(self):
    #     s = self.server_socket
    #     while True:
    #         client, address = s.accept()
    #         data = client.recv(self.buffer)
    #         data.decode('utf-8')
    #         print('received data: ', data)
    #         client.close()

    def client_handler(self):
        while True:
            to_read, to_write, errors = select.select(self.socket_list, [], [], 0) 
            for connection in to_read:
                if connection == self.server_socket:
                    client, address = self.server_socket.accept()
                    self.socket_list.append(client)
                    print(address, 'connected')
                    self.broadcast(client, '{0} entered the room\n'.format(address[0]))
                else:
                    data = connection.recv(self.buffer).decode()
                    if data and data[:5] == 'uname':
                        ip, port = connection.getpeername() 
                        self.unames[ip] = data[6:]
                        print('stored', ip, 'as user', data[6:])
                    elif data:
                        ip, port = connection.getpeername()
                        self.broadcast(connection, '\r' + '[' + self.unames[ip] + '] ' + data)
                    else:
                        ip, port = connection.getpeername()
                        print(ip, 'stored as', self.unames[ip], 'disconnected')
                        self.broadcast(connection, '\r' + self.unames[ip] + ' left\n')
                        connection.close()
                        self.socket_list.remove(connection)
    
    def broadcast(self, peer, text):
        for port in self.socket_list:
            if port not in (self.server_socket, peer):
                try:
                    text = text.encode()
                    port.send(text)
                except port.error as e:
                    print('error:', e)
                    port.close()
                    self.socket_list.remove(port)



