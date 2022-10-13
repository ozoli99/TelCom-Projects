from socket import socket, AF_INET, SOCK_STREAM
import struct
import random

server_addr = ('localhost', 10000)
packer = struct.Struct('c I')

operators = ['<', '>', '=']
last_num = last_n_num = last_i_num = 0
last_op = last_n_op = last_i_op = ''

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)

    lowest_num = 1
    highest_num = 100
    mid = round(lowest_num + (highest_num - lowest_num) // 2)
    sent_op = operators[mid % (len(operators) - 1)]

    packed_data = packer.pack(sent_op.encode(), int(mid))
    print('Client make starting guess')
    client.sendall(packed_data)

    while True:
        data = client.recv(1).decode()
        if data == 'V':
            print('Someone else won\nClient exits')
            client.close()
            exit(0)
        elif data == 'Y':
            print('Client won')
            client.close()
            exit(0)
        elif data == 'K':
            print('Client lose')
            client.close()
            exit(0)
        else:
            if data == 'I':
                if sent_op == '<':
                    highest_num = mid - 1
                elif sent_op == '>':
                    lowest_num = mid + 1
            if data == 'N':
                if sent_op == '<':
                    lowest_num = mid + 1
                elif sent_op == '>':
                    highest_num = mid - 1
            
            mid = round(lowest_num + (highest_num - lowest_num) // 2)
            
            if lowest_num == highest_num:
                sent_op = '='
            else:
                sent_op = operators[mid % (len(operators) - 1)]
            
            print('Client make another guess')
            packed_data = packer.pack(sent_op.encode(), int(mid))
            client.sendall(packed_data)