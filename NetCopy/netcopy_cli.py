from socket import socket,AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
from sys import argv
import struct
import hashlib

def send_file(connection, file_name):
    #print('Sending:', file_name)
    with open(file_name, 'rb') as file:
        raw = file.read()
    connection.sendall(len(raw).to_bytes(8, 'big'))
    connection.sendall(raw)
    return raw



netcopy_server_addr = (argv[1], int(argv[2]))
checksum_server_addr = (argv[3], int(argv[4]))
file_id = argv[5]
file_name = argv[6]

packer = struct.Struct('2s 1s i 1s i 1s i 1s 12s')

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(netcopy_server_addr)
	
    m = hashlib.md5()
    m.update(send_file(client, file_name))

    client.connect(checksum_server_addr)
    client.sendall(packer.pack('BE'.encode(), '|'.encode(), int(file_id), '|'.encode(), 60, '|'.encode(), 12, '|'.encode(), m.hexdigest()))