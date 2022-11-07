from socket import socket,AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
from select import select
from sys import argv
import struct

checksums = {}

checksum_server_addr = (argv[1], int(argv[2]))
file_name = argv[6]

unpacker = struct.Struct('2s 1s i 1s i 1s i 1s 12s')
packer = struct.Struct('i 1s 12s')

with socket(AF_INET, SOCK_STREAM) as checksum_server:
    checksum_server.bind(checksum_server_addr)
    checksum_server.listen(1)
    checksum_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    sockets = [checksum_server]

    while True:
        r,w,e = select(sockets,[],[],1)

        if not (r or w or e):
            continue
		
        for s in r:
            if s is checksum_server:
                # kliens csatlakozik
                netcopy_client, netcopy_client_addr = s.accept()
                sockets.append(netcopy_client)
                #print("Csatlakozott", netcopy_client_addr)
            else:
                data = s.recv(unpacker.size)
                # ha 0 byte akkor kilepett a kliens
                if not data:
                    sockets.remove(s)
                    s.close()
                    #print("Kilepett")
                else:
                    #print("Kaptam:",data)
                    unp_data = unpacker.unpack(data)
                    #print("Unpack:",unp_data)
                    file_id = unp_data[2]
                    result = ''
                    if unp_data[0].decode() == 'BE':
                        checksum = unp_data[8].decode()
                        checksums[file_id] = checksum
                        result = 'OK'
                        s.sendall(result.encode())
                    elif unp_data[0].decode() == 'KI':
                        if file_id in checksums.keys():
                            result = packer.pack(12, '|', checksums[file_id])
                        else:
                            result = packer.pack(0, '|', '')
                        s.sendall(result)
                    #print("Kiertekeltem es visszakuldtem", result)