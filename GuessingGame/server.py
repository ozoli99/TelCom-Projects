from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import select
import struct
import random

server_addr = ('', 10000)
unpacker = struct.Struct('c I')

correct_num = random.randint(1, 100)
answer = ''

print('Correct number:', correct_num)

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