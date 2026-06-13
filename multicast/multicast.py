import socket
import struct
import os

PORT = 5002

BUFFER_SIZE = 4096


# ================= PILIH GROUP =================

def pilih_group():

    print("\n=== PILIH GROUP MULTICAST ===")
    print("1. Grup A")
    print("2. Grup B")
    print("3. Grup C")

    pilihan = input("Pilih group: ")

    if pilihan == '1':
        return '224.1.1.1'

    elif pilihan == '2':
        return '224.1.1.2'

    elif pilihan == '3':
        return '224.1.1.3'

    else:
        return '224.1.1.1'


# ================= RECEIVER =================

def start_receiver(group):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    sock.bind(('', PORT))

    mreq = struct.pack(
        '4sl',
        socket.inet_aton(group),
        socket.INADDR_ANY
    )

    sock.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        mreq
    )

    print(f"Receiver multicast aktif di group {group}")

    while True:

        data, addr = sock.recvfrom(65535)

        print(f"\n[{group}] {data.decode()}")


# ================= SENDER =================

def start_sender():

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    return sock