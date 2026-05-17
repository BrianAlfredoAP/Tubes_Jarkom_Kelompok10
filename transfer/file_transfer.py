import os

BUFFER_SIZE = 4096


def send_file(client_socket, filepath):

    if not os.path.exists(filepath):

        print("[ERROR] File tidak ditemukan")
        return

    filename = os.path.basename(filepath)

    filesize = os.path.getsize(filepath)

    header = f"FILE|{filename}|{filesize}"

    client_socket.send(header.encode())

    with open(filepath, "rb") as file:

        while True:

            data = file.read(BUFFER_SIZE)

            if not data:
                break

            client_socket.sendall(data)

    print(f"[FILE SENT] {filename}")


def receive_file(
    client_socket,
    filename,
    filesize
):

    save_path = f"received_{filename}"

    with open(save_path, "wb") as file:

        remaining = filesize

        while remaining > 0:

            data = client_socket.recv(
                min(BUFFER_SIZE, remaining)
            )

            if not data:
                break

            file.write(data)

            remaining -= len(data)

    print(f"[FILE RECEIVED] {filename}")