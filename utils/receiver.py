import os
import socket
import struct
from datetime import datetime

BUFFER_SIZE = 4096

# ================= GET FOLDER =================

def get_folder(filename):

    ext = filename.split('.')[-1].lower()

    if ext in ['txt', 'pdf', 'docx']:
        return 'assets/dokumen'

    elif ext in ['jpg', 'jpeg', 'png']:
        return 'assets/gambar'

    elif ext in ['mp3', 'wav']:
        return 'assets/audio'

    elif ext in ['mp4', 'mov']:
        return 'assets/video'

    return 'assets'

# ================= RECEIVE TCP =================

def receive_tcp(sock):

    while True:

        try:

            # ================= RECEIVE HEADER =================

            header = b""

            while not header.endswith(b"\n"):

                chunk = sock.recv(1)

                if not chunk:

                    print("Koneksi terputus")
                    return

                header += chunk

            header = header.decode().strip()

            # ================= RECEIVE TEXT ===================

            if header.startswith("MSG|"):

                text = header[4:]

                try:

                    # ================= PARSE =================

                    username_start = text.find("[")
                    username_end = text.find("]")

                    username = text[
                        username_start + 1 : username_end
                    ]

                    metode = text.split("METODE:")[1] \
                                  .split("JENIS:")[0] \
                                  .strip()

                    jenis = text.split("JENIS:")[1] \
                                 .split("WAKTU:")[0] \
                                 .strip()

                    waktu = text.split("WAKTU:")[1] \
                                .split("ISI:")[0] \
                                .strip()

                    isi = text.split("ISI:")[1].strip()

                    # ================= OUTPUT =================

                    print("\n==============================")
                    print(f" WAKTU KIRIM    : {waktu}")
                    print(f" WAKTU DITERIMA : {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
                    print(f" USER           : {username}")
                    print(f" METODE         : {metode}")
                    print(f" JENIS          : {jenis}")
                    print(f" PESAN          : {isi}")
                    print("==============================")

                except Exception:

                    print("\nPesan diterima:")
                    print(text)

            # ================= RECEIVE FILE ===================

            elif header.startswith("FILE|"):

                info = header.split("|")

                filename = info[1]

                filesize = int(info[2])

                waktu = info[3]

                folder = get_folder(filename)

                os.makedirs(folder, exist_ok=True)

                filepath = os.path.join(
                    folder,
                    filename
                )

                waktu_mulai = datetime.now()

                print("\n==============================")
                print(f" WAKTU KIRIM      : {waktu}")
                print(f" MULAI TERIMA     : {waktu_mulai.strftime('%Y-%m-%d %H:%M:%S.%f')}")
                print(f" MENERIMA FILE     : {filename}")
                print(f" UKURAN FILE       : {filesize} byte")
                print("==============================")

                with open(filepath, 'wb') as f:

                    received = 0

                    while received < filesize:

                        data = sock.recv(
                            min(
                                BUFFER_SIZE,
                                filesize - received
                            )
                        )

                        if not data:
                            break

                        f.write(data)

                        received += len(data)

                        # ================= PROGRESS =================

                        progress = (
                            received / filesize
                        ) * 100

                        print(
                            f"\rProgress: {progress:.1f}%",
                            end=""
                        )

                print(f"\nFile berhasil diterima: {filename}")
                waktu_selesai = datetime.now()
                durasi = waktu_selesai - waktu_mulai
                print(f" WAKTU SELESAI   : {waktu_selesai.strftime('%Y-%m-%d %H:%M:%S.%f')}")
                print(f" DURASI TRANSFER : {durasi}")

            # ================= UNKNOWN DATA ===================

            else:

                print(f"\nData tidak dikenali: {header}")

        except Exception as e:

            print("Receive Error:", e)

            break


def create_multicast_socket(port):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
        socket.IPPROTO_UDP
    )

    sock.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    try:
        sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEPORT,
            1
        )
    except Exception:
        pass

    sock.bind(('', port))

    for group in ['224.1.1.1', '224.1.1.2', '224.1.1.3']:
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

    return sock


def create_broadcast_socket(port):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    sock.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    try:
        sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEPORT,
            1
        )
    except Exception:
        pass

    sock.bind(('', port))

    return sock


def receive_multicast(sock):

    print("[CLIENT MULTICAST] Receiver aktif")

    while True:

        data, addr = sock.recvfrom(65535)

        if data.startswith(b"FILE|"):

            try:

                header = data.decode().strip()

                parts = header.split("|")

                filename = parts[1]
                filesize = int(parts[2])
                waktu = parts[3] if len(parts) > 3 else 'Unknown'

                folder = get_folder(filename)
                os.makedirs(folder, exist_ok=True)
                filepath = os.path.join(folder, filename)

                waktu_mulai = datetime.now()

                print("\n==============================")
                print(f" WAKTU KIRIM      : {waktu}")
                print(f" MULAI TERIMA     : {waktu_mulai.strftime('%Y-%m-%d %H:%M:%S.%f')}")
                print(f" MENERIMA FILE     : {filename}")
                print(f" UKURAN FILE       : {filesize} byte")
                print("==============================")

                with open(filepath, 'wb') as f:

                    received = 0

                    while received < filesize:

                        chunk, _ = sock.recvfrom(BUFFER_SIZE)

                        if not chunk:
                            break

                        f.write(chunk)
                        received += len(chunk)

                        progress = (received / filesize) * 100
                        print(f"\rProgress: {progress:.1f}%", end="")

                waktu_selesai = datetime.now()
                durasi = waktu_selesai - waktu_mulai
                print(f"\nFile berhasil diterima: {filename}")
                print(f" WAKTU SELESAI   : {waktu_selesai.strftime('%Y-%m-%d %H:%M:%S.%f')}")
                print(f" DURASI TRANSFER : {durasi}")

            except Exception as e:
                print("[CLIENT MULTICAST] Error menerima file:", e)

        else:
            try:
                print(f"\n[MULTICAST] {data.decode()}")
            except UnicodeDecodeError:
                print("\n[MULTICAST] Binary data diterima")


def receive_broadcast(sock):

    print("[CLIENT BROADCAST] Receiver aktif")

    while True:

        data, addr = sock.recvfrom(65535)

        if data.startswith(b"FILE|"):

            try:

                header = data.decode().strip()

                parts = header.split("|")

                filename = parts[1]
                filesize = int(parts[2])
                waktu = parts[3] if len(parts) > 3 else 'Unknown'

                folder = get_folder(filename)
                os.makedirs(folder, exist_ok=True)
                filepath = os.path.join(folder, filename)

                waktu_mulai = datetime.now()

                print("\n==============================")
                print(f" WAKTU KIRIM      : {waktu}")
                print(f" MULAI TERIMA     : {waktu_mulai.strftime('%Y-%m-%d %H:%M:%S.%f')}")
                print(f" MENERIMA FILE     : {filename}")
                print(f" UKURAN FILE       : {filesize} byte")
                print("==============================")

                with open(filepath, 'wb') as f:

                    received = 0

                    while received < filesize:

                        chunk, _ = sock.recvfrom(BUFFER_SIZE)

                        if not chunk:
                            break

                        f.write(chunk)
                        received += len(chunk)

                        progress = (received / filesize) * 100
                        print(f"\rProgress: {progress:.1f}%", end="")

                waktu_selesai = datetime.now()
                durasi = waktu_selesai - waktu_mulai
                print(f"\nFile berhasil diterima: {filename}")
                print(f" WAKTU SELESAI   : {waktu_selesai.strftime('%Y-%m-%d %H:%M:%S.%f')}")
                print(f" DURASI TRANSFER : {durasi}")

            except Exception as e:
                print("[CLIENT BROADCAST] Error menerima file:", e)

        else:
            try:
                print(f"\n[BROADCAST] {data.decode()}")
            except UnicodeDecodeError:
                print("\n[BROADCAST] Binary data diterima")
