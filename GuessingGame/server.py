from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import select

server_addr = ('', 10000)

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
                client_conn.setblocking(0)

                sockets.append(client_conn)
            else:           # handle client
                data = s.recv(1024)
                if not data:
                    sockets.remove(s)
                    if s in writables:
                        writables.remove(s)
                    s.close()