import socket

PORT = 5003


def start_receiver():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind(('', PORT))

    return sock


def start_sender():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_BROADCAST,
        1
    )

    return sock