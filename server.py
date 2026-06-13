# FILE: server.py

import socket
import threading

# ================= CONFIG =================

HOST = '127.0.0.1'
PORT = 5000

MULTICAST_GROUP = '224.1.1.1'
MULTICAST_PORT = 5002

BROADCAST_PORT = 5003

BUFFER_SIZE = 4096

# MODE:
# single / multi

MODE = "multi"

# ================= TCP SERVER =================

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

server.listen()

print(f"[TCP] Server aktif di port {PORT}")
print(f"[MODE] {MODE}")

clients = []
clients_lock = threading.Lock()

# ================= BROADCAST TCP =================

def broadcast_tcp(data, sender):

    with clients_lock:

        for client in clients[:]:

            if client != sender:

                try:

                    client.sendall(data)

                except:

                    clients.remove(client)

# ================= HANDLE CLIENT =================

def handle_client(conn, addr):

    print(f"[TCP] Client masuk: {addr}")

    while True:

        try:

            data = conn.recv(BUFFER_SIZE)

            if not data:
                break

            broadcast_tcp(data, conn)

        except:
            break

    with clients_lock:

        if conn in clients:
            clients.remove(conn)

    conn.close()

    print(f"[TCP] Client keluar: {addr}")

# ================= TCP LOOP =================

while True:

    conn, addr = server.accept()

    with clients_lock:
        clients.append(conn)

    # ================= SINGLE THREAD =================

    if MODE == "single":

        handle_client(conn, addr)

    # ================= MULTITHREAD =================

    else:

        threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        ).start()