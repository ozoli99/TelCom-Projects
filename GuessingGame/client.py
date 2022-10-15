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
    mid = lowest_num + (highest_num - lowest_num) // 2
    sent_op = operators[mid % (len(operators) - 1)]
    range_nums = [mid]

    packed_data = packer.pack(sent_op.encode(), int(mid))
    print('Client make starting guess')
    client.sendall(packed_data)

    while True:
        data = client.recv(packer.size)
        unp_data = packer.unpack(data)
        if unp_data[0].decode() == 'V':
            print('Someone else won\nClient exits')
            client.close()
            exit(0)
        elif unp_data[0].decode() == 'Y':
            print('Client won')
            client.close()
            exit(0)
        elif unp_data[0].decode() == 'K':
            print('Client lose')
            client.close()
            exit(0)
        else:
            if unp_data[0].decode() == 'I':
                if sent_op == '<':
                    highest_num = mid - 1
                elif sent_op == '>':
                    lowest_num = mid + 1
            if unp_data[0].decode() == 'N':
                if sent_op == '<':
                    lowest_num = mid + 1
                elif sent_op == '>':
                    highest_num = mid - 1
            
            mid = lowest_num + (highest_num - lowest_num) // 2

            if mid in range_nums:
                sent_op = '='
            else:
                range_nums.append(mid)
            
            if lowest_num >= highest_num:
                sent_op = '='
            else:
                sent_op = operators[mid % (len(operators) - 1)]
            
            print('Client make another guess')
            packed_data = packer.pack(sent_op.encode(), int(mid))
            client.sendall(packed_data)