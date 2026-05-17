import os

from shared.config import BUFFER_SIZE

DOWNLOAD_FOLDER = "storage/downloads"


def handle_file(client_socket, data):
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