import socket
import struct
import os

PORT = 5002
BUFFER_SIZE = 4096

print("\n=== PILIH GROUP MULTICAST ===")
print("1. Grup A")
print("2. Grup B")
print("3. Grup C")

pilihan = input("Pilih grup: ")

if pilihan == '1':
    MULTICAST_GROUP = '224.1.1.1'
elif pilihan == '2':
    MULTICAST_GROUP = '224.1.1.2'
elif pilihan == '3':
    MULTICAST_GROUP = '224.1.1.3'
else:
    MULTICAST_GROUP = '224.1.1.1'

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

sock.bind(('', PORT))

mreq = struct.pack(
    '4sl',
    socket.inet_aton(MULTICAST_GROUP),
    socket.INADDR_ANY
)

sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq
)

print(f"\nReceiver multicast aktif di {MULTICAST_GROUP}")

while True:

    data, addr = sock.recvfrom(65535)

    # HEADER FILE
    if data.startswith(b"FILE|"):

        try:

            header = data.decode().strip()

            _, filename, filesize = header.split("|")

            filesize = int(filesize)

            os.makedirs("assets/received_multicast", exist_ok=True)

            filepath = os.path.join(
                "assets/received_multicast",
                filename
            )

            print(f"\nMenerima file: {filename}")
            print(f"Ukuran: {filesize} byte")

            received = 0

            with open(filepath, "wb") as f:

                while received < filesize:

                    chunk, _ = sock.recvfrom(BUFFER_SIZE)

                    f.write(chunk)

                    received += len(chunk)

                    progress = (
                        received / filesize
                    ) * 100

                    print(
                        f"\rProgress: {progress:.1f}%",
                        end=""
                    )

            print(f"\nFile tersimpan: {filepath}")

        except Exception as e:

            print("Error menerima file:", e)

    else:

        try:

            print(f"\n[{MULTICAST_GROUP}] {data.decode()}")

        except UnicodeDecodeError:

            print("Data tidak dikenali")