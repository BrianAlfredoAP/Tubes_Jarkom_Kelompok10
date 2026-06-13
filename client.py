# =========================
# FILE: client.py
# =========================

import socket
import threading
import os
from datetime import datetime

from utils.menu import (
    pilih_metode,
    pilih_data
)
from multicast.multicast import pilih_group

from utils.sender import (
    send_text,
    send_file
)

from utils.receiver import (
    receive_tcp,
    create_multicast_socket,
    create_broadcast_socket,
    receive_multicast,
    receive_broadcast
)

# ================= CONFIG =================

HOST = '127.0.0.1'
PORT = 5000

MULTICAST_PORT = 5002
BROADCAST_PORT = 5003

BUFFER_SIZE = 4096

# ================= USER =================

username = input("Masukkan username: ")

# ================= TCP CLIENT =================

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect((HOST, PORT))

# ================= ASSETS =================

os.makedirs("assets/dokumen", exist_ok=True)
os.makedirs("assets/gambar", exist_ok=True)
os.makedirs("assets/audio", exist_ok=True)
os.makedirs("assets/video", exist_ok=True)

# ================= RECEIVE THREAD =================

threading.Thread(
    target=receive_tcp,
    args=(client,),
    daemon=True
).start()

multicast_recv_sock = create_multicast_socket(MULTICAST_PORT)
threading.Thread(
    target=receive_multicast,
    args=(multicast_recv_sock,),
    daemon=True
).start()

broadcast_recv_sock = create_broadcast_socket(BROADCAST_PORT)
threading.Thread(
    target=receive_broadcast,
    args=(broadcast_recv_sock,),
    daemon=True
).start()

# ================= MENU LOOP =================

while True:

    metode = pilih_metode()
    jenis = pilih_data()

    multicast_group = None
    multicast_socket = None
    broadcast_socket = None

    # ================= METODE =================

    if metode == '1':

        metode_text = "SINGLE THREAD"

    elif metode == '2':

        metode_text = "MULTITHREAD"

    elif metode == '3':

        metode_text = "MULTICAST"

        multicast_group = pilih_group()

        multicast_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
            socket.IPPROTO_UDP
        )

        multicast_socket.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_MULTICAST_TTL,
            2
        )

        print(f"Group aktif: {multicast_group}")

    elif metode == '4':

        metode_text = "BROADCAST"

        broadcast_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        broadcast_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_BROADCAST,
            1
        )

    else:

        print("Metode tidak valid")
        continue

    print("\nKetik 'exit' untuk kembali")

    # ================= CHAT LOOP =================

    while True:

        pesan = input("Kirim: ")

        if pesan.lower() == 'exit':

            print("\nKembali ke menu...\n")

            break

        # ==================================================
        # ================= KIRIM TEXT =====================
        # ==================================================

        if jenis == '1':

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

            # ================= MULTICAST =================

            if metode == '3':

                message = (
                    f"MSG|"
                    f"[{username}] "
                    f"METODE:{metode_text} "
                    f"JENIS:TEXT "
                    f"WAKTU:{timestamp} "
                    f"ISI:{pesan}\n"
                )

                multicast_socket.sendto(
                    message.encode(),
                    (multicast_group, MULTICAST_PORT)
                )

                print("Pesan multicast terkirim")

            # ================= BROADCAST =================

            elif metode == '4':

                message = (
                    f"MSG|"
                    f"[{username}] "
                    f"METODE:{metode_text} "
                    f"JENIS:TEXT "
                    f"WAKTU:{timestamp} "
                    f"ISI:{pesan}\n"
                )

                broadcast_socket.sendto(
                    message.encode(),
                    ('<broadcast>', BROADCAST_PORT)
                )

                print("Pesan broadcast terkirim")

            # ================= TCP =================

            else:

                send_text(
                    client,
                    username,
                    metode_text,
                    "TEXT",
                    pesan
                )

        # ==================================================
        # ================= KIRIM FILE =====================
        # ==================================================

        elif jenis == '2':

            pesan = pesan.strip('"').strip("'")

            if not os.path.exists(pesan):

                print("File tidak ditemukan")

                continue

            # ================= MULTICAST =================

            if metode == '3':

                filename = os.path.basename(pesan)

                filesize = os.path.getsize(pesan)

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

                header = f"FILE|{filename}|{filesize}|{timestamp}\n"

                multicast_socket.sendto(
                    header.encode(),
                    (multicast_group, MULTICAST_PORT)
                )

                with open(pesan, 'rb') as f:

                    while True:

                        data = f.read(BUFFER_SIZE)

                        if not data:
                            break

                        multicast_socket.sendto(
                            data,
                            (multicast_group, MULTICAST_PORT)
                        )

                print(f"File multicast terkirim: {filename}")

            # ================= BROADCAST =================

            elif metode == '4':

                filename = os.path.basename(pesan)

                filesize = os.path.getsize(pesan)

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

                header = f"FILE|{filename}|{filesize}|{timestamp}\n"

                broadcast_socket.sendto(
                    header.encode(),
                    ('<broadcast>', BROADCAST_PORT)
                )

                with open(pesan, 'rb') as f:

                    while True:

                        data = f.read(BUFFER_SIZE)

                        if not data:
                            break

                        broadcast_socket.sendto(
                            data,
                            ('<broadcast>', BROADCAST_PORT)
                        )

                print(f"File broadcast terkirim: {filename}")

            # ================= TCP =================

            else:

                send_file(
                    client,
                    pesan
                )

        else:

            print("Jenis data tidak valid")