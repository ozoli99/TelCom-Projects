from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import select
import struct
import random
import sys

class SimpleTCPSelectServer:
    def __init__(self, addr='localhost', port=10001, timeout=1):
        self.server = self.setupServer(addr, port)
        # Sockets from which we expect to read
        self.inputs = [self.server]
        # Wait for at least one of the sockets to be ready for processing
        self.timeout = timeout

    def setupServer(self, addr, port):
        # Create a TCP/IP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the port
        server_address = (addr, port)
        server.bind(server_address)

        # Listen for incoming connections
        server.listen(5)
        return server

    def handleNewConnection(self, sock):
        # A "readable" server socket is ready to accept a connection
        connection, client_address = sock.accept()
        connection.setblocking(0)   # or connection.settimeout(1.0)
        self.inputs.append(connection)

    def handleDataFromClient(self, sock):
        data = sock.recv(1024)
        if data:
            sock.sendall(b'OK')
        else:
            # Interpret empty result as closed connection
            # Stop listening for input on the connection
            self.inputs.remove(sock)
            sock.close()

    def handleInputs(self, readable):
        for sock in readable:
            if sock is self.server:
                self.handleNewConnection(sock)
            else:
                self.handleDataFromClient(sock)

    def handleExceptionalCondition(self, exceptional):
        for sock in exceptional:
            # Stop listening for input on the connection
            self.inputs.remove(sock)
            sock.close()

    def handleConnections(self):
        while self.inputs:
            try:
                readable, writable, exceptional = select.select(self.inputs, [], self.inputs, self.timeout)
                
                if not (readable or writable or exceptional):
                    continue

                self.handleInputs(readable)
                self.handleExceptionalCondition(exceptional)
            except KeyboardInterrupt:
                print("The server stops")
                for c in self.inputs:
                    c.close()
                self.inputs = []

if len(sys.argv) == 3:
    simpleTCPSelectServer = SimpleTCPSelectServer(sys.argv[1], int(sys.argv[2]))
else:
    simpleTCPSelectServer = SimpleTCPSelectServer()
simpleTCPSelectServer.handleConnections()

server_addr = ('', 10000)
unpacker = struct.Struct('c I')

correct_num = random.randint(1, 100)
answer = ''

print('Correct number:', correct_num)

with socket(AF_INET, SOCK_STREAM) as server:
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(server_addr)
    server.listen(5)

    sockets = [server]

    while True:
        readables, writables, exceptionals = select.select(sockets, sockets, sockets, 1)

        if not (readables or writables or exceptionals):
            continue

        for s in readables:
            if s is server: # new client connect
                client_conn, client_addr = s.accept()
                client_conn.setblocking(0)

                print('Connected:', client_addr)
                
                sockets.append(client_conn)
            else:           # handle client
                data = s.recv(unpacker.size)
                if not data:
                    sockets.remove(s)
                    s.close()
                    print('Exited')
                else:
                    print('Received:', data)
                    unp_data = unpacker.unpack(data)
                    print('Unpack:', unp_data)
                    if answer == 'Y':
                        answer = 'V'
                    else:
                        if unp_data[0].decode() == '=':
                            if int(unp_data[1]) == correct_num:
                                answer = 'Y'
                            else:
                                answer = 'K'
                        elif unp_data[0].decode() == '>':
                            if correct_num > int(unp_data[1]):
                                answer = 'I'
                            else:
                                answer = 'N'
                        elif unp_data[0].decode() == '<':
                            if correct_num < int(unp_data[1]):
                                answer = 'I'
                            else:
                                answer = 'N'
                    print('Evaluated and sent back', answer)
                    s.sendall(str(answer).encode())