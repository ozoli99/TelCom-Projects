from socket import socket, AF_INET, SOCK_STREAM

server_addr = ('localhost', 10000)

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)
    client.sendall(b'Hello Server!')
    data = client.recv(1024)