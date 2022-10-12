from socket import socket, AF_INET, SOCK_STREAM

server_addr = ('', 10000)

with socket(AF_INET, SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen()
    client_conn, client_addr = server.accept()
    with client_conn:
        while True:
            data = client_conn.recv(1024)
            if not data:
                break
            client_conn.sendall(data)