import socket

HOST = '127.0.0.1'
PORT = 5001


def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))

    server.listen(5)

    print("Multithread Server Aktif")

    conn, addr = server.accept()

    print("Client:", addr)

    return conn


def start_client():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((HOST, PORT))

    return client