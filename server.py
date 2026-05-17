import socket
import threading
from unicast.multithread import handle_client

HOST = "0.0.0.0"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server.bind((HOST, PORT))
server.listen(10)

clients = {}

print(f"[SERVER] Running on {PORT}")

while True:

    client_socket, address = server.accept()

    username = client_socket.recv(1024).decode()

    clients[username] = client_socket

    print(f"[CONNECTED] {username}")
    print(clients.keys())

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, username, clients)
    )

    thread.start()