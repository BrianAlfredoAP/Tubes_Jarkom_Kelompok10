# FILE: utils/sender.py

import os
from datetime import datetime

BUFFER_SIZE = 4096

# ================= SEND TEXT =================

def send_text(sock, username, metode, jenis, pesan):

    try:

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        # ================= PACKET =================
        # dibuat satu baris agar receiver
        # tidak membaca per line

        packet = (
            f"MSG|"
            f"[{username}] "
            f"METODE:{metode} "
            f"JENIS:{jenis} "
            f"WAKTU:{timestamp} "
            f"ISI:{pesan}\n"
        )

        # ================= SEND =================

        sock.sendall(packet.encode())

        print(f"Pesan berhasil dikirim pada {timestamp}")

    except Exception as e:

        print("Send Text Error:", e)

# ================= SEND FILE =================

def send_file(sock, filepath):

    try:

        # ================= VALIDASI FILE =================

        if not os.path.exists(filepath):

            print("File tidak ditemukan")
            return

        # ================= FILE INFO =================

        filename = os.path.basename(filepath)

        filesize = os.path.getsize(filepath)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        # ================= HEADER =================

        header = f"FILE|{filename}|{filesize}|{timestamp}\n"

        sock.sendall(header.encode())

        # ================= SEND FILE =================

        with open(filepath, 'rb') as f:

            sent = 0

            while sent < filesize:

                data = f.read(BUFFER_SIZE)

                if not data:
                    break

                sock.sendall(data)

                sent += len(data)

        print(f"File berhasil dikirim: {filename}")

    except Exception as e:

        print("Send File Error:", e)