from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import select
import struct

server_addr = ('', 10000)
unpacker = struct.Struct('c I')

with socket(AF_INET, SOCK_STREAM) as server:
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(server_addr)
    server.listen()

    sockets = [server]

    while True:
        readables, writables, exceptionals = select.select(sockets, sockets, sockets, 1)

        if not (readables or writables or exceptionals):
            continue

        for s in readables:
            if s is server: # new client connect
                client_conn, client_addr = s.accept()
                sockets.append(client_conn)
            else:           # handle client
                data = s.recv(unpacker.size)
                if not data:
                    sockets.remove(s)
                    s.close()
                else:
                    unp_data = unpacker.unpack(data)
                    