import socket

from shared.config import HOST, PORT
from server.managers.thread_manager import start_client_thread

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, address = server_socket.accept()

    print(f"Connection from {address}")

    start_client_thread(client_socket)