from socket import socket, AF_INET, SOCK_STREAM
import struct
import random

server_addr = ('localhost', 10000)
packer = struct.Struct('c I')

operators = ['<', '>', '=']
num = 0
op = ''

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)

    start_num = random.randint(1, 100)
    start_op = operators[start_num % len(operators)]
    num = start_num
    op = start_op

    packed_data = packer.pack((start_op.encode(), int(start_num)))

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
                if op == '<':
                    num = random.randint(1, num)
                    op = operators[num % len(operators)]
                elif op == '>':
                    num = random.randint(num, 100)
                    op = operators[num % len(operators)]
            elif data == 'N':
                if op == '<':
                    num = random.randint(num, 100)
                    op = operators[num % len(operators)]
                elif op == '>':
                    num = random.randint(1, num)
                    op = operators[num % len(operators)]
            packed_data = packer.pack((op.encode(), int(num)))
            client.sendall(packed_data)