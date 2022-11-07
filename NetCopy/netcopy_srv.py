from socket import socket,AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct
from sys import argv

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



server_addr = (argv[1], int(argv[2]))
file_name = argv[6]

with socket(AF_INET, SOCK_STREAM) as server:
	server.bind(server_addr)
	server.listen(1)
	server.settimeout(1.0)
	
	while True:
		try:
			client, client_addr = server.accept()
			print("Csatlakozott: ", client_addr)

            recv_file(client, file_name)

            # Fajl ellenorzes Checksum szerverrel
            # Hiba eseten a stdout-ra ki kell irni: CSUM CORRUPTED
            # Helyes atvitel eseten az stdout-ra ki kell irni: CSUM OK
		except timeout:
			pass