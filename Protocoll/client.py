import sys
import struct

file1 = sys.argv[1]
file2 = sys.argv[2]
file3 = sys.argv[3]
file4 = sys.argv[4]

# file1
packer = struct.Struct('? c 9s')
with open(file1, 'rb') as file:
    data = file.read(packer.size)
    print(packer.unpack(data))

# file2
packer = struct.Struct('9s i f')
with open(file2, 'rb') as file:
    data = file.read(packer.size)
    print(packer.unpack(data))

# file3
packer = struct.Struct('f c ?')
with open(file3, 'rb') as file:
    data = file.read(packer.size)
    print(packer.unpack(data))

# file4
packer = struct.Struct('9s ? i')
with open(file4, 'rb') as file:
    data = file.read(packer.size)
    print(packer.unpack(data))

# "elso"(15), 73, True
packer = struct.Struct('15s i ?')
values = ('elso', 73, True)
print(packer.pack(*values))

# 76.5, False, 'X'
packer = struct.Struct('f ? c')
values = (76.5, False, 'X')
print(packer.pack(*values))

# 64, "masodik"(13), 83.9
packer = struct.Struct('i 13s f')
values = (64, 'masodik', 83.9)
print(packer.pack(*values))

# 'Z', 95, "harmadik"(16)
packer = struct.Struct('c i 16s')
values = ('Z', 95, 'harmadik')
print(packer.pack(*values))