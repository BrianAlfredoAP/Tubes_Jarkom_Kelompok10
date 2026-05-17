import os

from shared.protocol import create_message
from shared.config import BUFFER_SIZE, ENCODING


def upload_file(client_socket, sender, target, filepath):

    if not os.path.exists(filepath):
        print("[ERROR] File not found")
        return

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    print(f"\nUploading file: {filename}")
    print(f"File size: {filesize} bytes")
    print(f"Sending to {target}...")

    metadata = create_message(
        msg_type="FILE",
        sender=sender,
        target=target,
        filename=filename,
        filesize=filesize
    )

    client_socket.send(metadata.encode(ENCODING))

    with open(filepath, "rb") as file:

        while True:

            bytes_read = file.read(BUFFER_SIZE)

            if not bytes_read:
                break

            client_socket.send(bytes_read)

    print(f"[SUCCESS] File {filename} sent successfully")