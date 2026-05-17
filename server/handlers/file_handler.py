import os

from shared.config import BUFFER_SIZE
from server.managers.client_manager import get_client


DOWNLOAD_FOLDER = "storage/downloads"


def handle_file(client_socket, data):
    target_socket = get_client(data["target"])

    filename = data["filename"]
    filesize = data["filesize"]

    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    received_size = 0

    with open(filepath, "wb") as file:
        while received_size < filesize:
            bytes_read = client_socket.recv(BUFFER_SIZE)

            if not bytes_read:
                break

            file.write(bytes_read)
            received_size += len(bytes_read)

    print(f"File {filename} received")

    if target_socket:
        with open(filepath, "rb") as file:
            while True:
                bytes_read = file.read(BUFFER_SIZE)

                if not bytes_read:
                    break

                target_socket.send(bytes_read)