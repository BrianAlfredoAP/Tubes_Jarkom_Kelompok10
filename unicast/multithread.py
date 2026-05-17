from unicast.single_thread import unicast_single
from multicast.multicast import multicast_message
from broadcast.broadcast import broadcast_message
from transfer.file_transfer import receive_file


def handle_client(client_socket, username, clients):

    while True:

        try:

            message = client_socket.recv(4096)

            if not message:
                break

            # FILE
            if message.startswith(b"FILE|"):

                header = message.decode()

                _, filename, filesize = header.split("|")

                filesize = int(filesize)

                receive_file(
                    client_socket,
                    filename,
                    filesize
                )

                continue

            message = message.decode()

            # UNICAST
            if message.startswith("/unicast"):

                parts = message.split(" ", 2)

                target = parts[1]
                msg = parts[2]

                unicast_single(
                    username,
                    target,
                    msg,
                    clients
                )

            # MULTICAST
            elif message.startswith("/multicast"):

                parts = message.split(" ", 2)

                targets = parts[1].split(",")
                msg = parts[2]

                multicast_message(
                    username,
                    targets,
                    msg,
                    clients
                )

            # BROADCAST
            elif message.startswith("/broadcast"):

                msg = message.replace(
                    "/broadcast ",
                    ""
                )

                broadcast_message(
                    username,
                    msg,
                    clients
                )

        except Exception as e:

            print(f"[ERROR] {e}")
            break

    print(f"[DISCONNECTED] {username}")

    del clients[username]

    client_socket.close()