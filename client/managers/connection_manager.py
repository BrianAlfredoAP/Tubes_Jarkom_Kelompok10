import socket

from shared.config import HOST, PORT


def connect_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print(f"Connected to server {HOST}:{PORT}")

    return client_socket