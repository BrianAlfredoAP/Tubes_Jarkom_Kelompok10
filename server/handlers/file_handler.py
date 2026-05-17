import os

from shared.config import BUFFER_SIZE
from server.managers.client_manager import get_client, get_all_clients


DOWNLOAD_FOLDER = "storage/downloads"


def _receive_file(client_socket, filepath, filesize):
    """Terima file dari client dan simpan ke disk."""
    received_size = 0

    with open(filepath, "wb") as file:
        while received_size < filesize:
            bytes_read = client_socket.recv(BUFFER_SIZE)

            if not bytes_read:
                break

            file.write(bytes_read)
            received_size += len(bytes_read)


def _send_file_to_socket(filepath, target_socket):
    """Kirim file ke satu socket tujuan."""
    with open(filepath, "rb") as file:
        while True:
            bytes_read = file.read(BUFFER_SIZE)

            if not bytes_read:
                break

            target_socket.send(bytes_read)


def handle_file(client_socket, data):
    filename = data["filename"]
    filesize = data["filesize"]
    target_field = data["target"]
    sender = data["sender"]

    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    # Terima file dari pengirim
    _receive_file(client_socket, filepath, filesize)

    print(f"[FILE] File {filename} diterima dari {sender}")

    # --- UNICAST: satu target ---
    if target_field and target_field != "ALL" and "," not in target_field:
        target_socket = get_client(target_field)

        if target_socket:
            _send_file_to_socket(filepath, target_socket)
            print(f"[FILE] File {filename} diteruskan ke {target_field}")
        else:
            print(f"[FILE] Target {target_field} tidak ditemukan")

    # --- MULTICAST: beberapa target (dipisahkan koma) ---
    elif target_field and target_field != "ALL" and "," in target_field:
        targets = [t.strip() for t in target_field.split(",") if t.strip()]
        sent_count = 0

        for target in targets:
            target_socket = get_client(target)

            if target_socket:
                try:
                    _send_file_to_socket(filepath, target_socket)
                    sent_count += 1
                except Exception as error:
                    print(f"[MULTICAST FILE] Gagal kirim ke {target}: {error}")
            else:
                print(f"[MULTICAST FILE] Target {target} tidak ditemukan")

        print(f"[MULTICAST FILE] File {filename} dikirim ke {sent_count}/{len(targets)} target")

    # --- BROADCAST: semua client ---
    elif target_field == "ALL":
        all_clients = get_all_clients()
        sent_count = 0

        for username, target_socket in all_clients.items():
            if username == sender:
                continue

            try:
                _send_file_to_socket(filepath, target_socket)
                sent_count += 1
            except Exception as error:
                print(f"[BROADCAST FILE] Gagal kirim ke {username}: {error}")

        print(f"[BROADCAST FILE] File {filename} dikirim ke {sent_count} client")