import socket

HOST = '127.0.0.1'
PORT = 5000

BUFFER_SIZE = 4096


# ================= SINGLE THREAD SERVER =================

def start_server():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))

    # HANYA 1 CLIENT
    server.listen(1)

    print("Single Thread Server Aktif")

    while True:

        # ================= TERIMA CLIENT =================

        conn, addr = server.accept()

        print(f"Client terhubung: {addr}")

        # ================= HANDLE CLIENT =================

        while True:

            try:

                data = conn.recv(BUFFER_SIZE)

                if not data:
                    break

                try:

                    print(f"Pesan: {data.decode()}")

                except:

                    print("Binary data diterima")

                # ECHO BALIK
                conn.sendall(data)

            except Exception as e:

                print("Error:", e)

                break

        print(f"Client keluar: {addr}")

        conn.close()


# ================= SINGLE THREAD CLIENT =================

def start_client():

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client.connect((HOST, PORT))

    print("Terhubung ke server single thread")

    return client