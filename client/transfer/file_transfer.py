import os

from shared.protocol import create_message
from shared.config import BUFFER_SIZE, ENCODING


def _send_file_bytes(client_socket, filepath):
    """Kirim raw bytes file ke server."""
    with open(filepath, "rb") as file:
        while True:
            bytes_read = file.read(BUFFER_SIZE)

            if not bytes_read:
                break

            client_socket.send(bytes_read)


def upload_file(client_socket, sender, target, filepath):
    """Unicast: kirim file ke satu target."""
    if not os.path.exists(filepath):
        print("[ERROR] File tidak ditemukan")
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
    _send_file_bytes(client_socket, filepath)

    print(f"[SUCCESS] File {filename} berhasil dikirim ke {target}")


def upload_file_multicast(client_socket, sender, targets, filepath):
    """Multicast: kirim file ke beberapa target (list username)."""
    if not os.path.exists(filepath):
        print("[ERROR] File tidak ditemukan")
        return

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    target_str = ",".join(targets)

    print(f"\nUploading file: {filename}")
    print(f"File size: {filesize} bytes")
    print(f"Sending ke {len(targets)} target: {target_str}...")

    metadata = create_message(
        msg_type="FILE",
        sender=sender,
        target=target_str,
        filename=filename,
        filesize=filesize
    )

    client_socket.send(metadata.encode(ENCODING))
    _send_file_bytes(client_socket, filepath)

    print(f"[SUCCESS] File {filename} berhasil dikirim (multicast)")


def upload_file_broadcast(client_socket, sender, filepath):
    """Broadcast: kirim file ke semua client."""
    if not os.path.exists(filepath):
        print("[ERROR] File tidak ditemukan")
        return

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    print(f"\nUploading file: {filename}")
    print(f"File size: {filesize} bytes")
    print(f"Broadcasting ke semua client...")

    metadata = create_message(
        msg_type="FILE",
        sender=sender,
        target="ALL",
        filename=filename,
        filesize=filesize
    )

    client_socket.send(metadata.encode(ENCODING))
    _send_file_bytes(client_socket, filepath)

    print(f"[SUCCESS] File {filename} berhasil di-broadcast")
