from socket import socket,AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
from sys import argv
import struct

def recv_file(connection, file_name):
    expected_size = b""
    while len(expected_size) < 8:
        more_size = conn.recv(8 - len(expected_size))
        if not more_size:
            raise Exception("Short file length received")
        expected_size += more_size

    expected_size = int.from_bytes(expected_size, 'big')

    packet = b''
    while len(packet) < expected_size:
        buffer = connection.recv(expected_size - len(packet))
        if not buffer:
            raise Exception('Incomplete file received')
        packet += buffer
    with open(file_name, 'wb') as file:
        file.write(packet)



netcopy_server_addr = (argv[1], int(argv[2]))
checksum_server_addr = (argv[3], int(argv[4]))
file_id = argv[5]
file_name = argv[6]

packer = struct.Struct('2s 1s i')
unpacker = struct.Struct('i 1s 12s')

with socket(AF_INET, SOCK_STREAM) as netcopy_server:
    netcopy_server.bind(netcopy_server_addr)
    netcopy_server.listen(1)
    netcopy_server.settimeout(1.0)

    while True:
        try:
            netcopy_client, netcopy_client_addr = netcopy_server.accept()
            #print("Csatlakozott: ", netcopy_client_addr)

            recv_file(netcopy_client, file_name)

            netcopy_server.connect(checksum_server_addr)
            netcopy_server.sendall(packer.pack('KI'.encode(), '|'.encode(), int(file_id)))

            data = netcopy_server.recv(unpacker.size)
            data = unpacker.unpack(data)

            if data[0] == 0:
                print('CSUM CORRUPTED')
            else:
                print('CSUM OK')

        except timeout:
            pass