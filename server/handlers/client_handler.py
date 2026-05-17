from shared.config import BUFFER_SIZE, ENCODING
from shared.protocol import parse_message, UNICAST, MULTICAST, BROADCAST, FILE

from server.handlers.unicast_handler import handle_unicast
from server.handlers.multicast_handler import handle_multicast
from server.handlers.broadcast_handler import handle_broadcast
from server.handlers.file_handler import handle_file
from server.managers.client_manager import add_client, remove_client

clients_username = {}


def handle_client(client_socket):
    username = client_socket.recv(BUFFER_SIZE).decode(ENCODING)

    clients_username[client_socket] = username

    add_client(username, client_socket)

    print(f"{username} connected")

    while True:
        try:
            raw_data = client_socket.recv(BUFFER_SIZE)

            if not raw_data:
                break

            data = parse_message(raw_data.decode(ENCODING))

            if data["type"] == UNICAST:
                handle_unicast(data)

            elif data["type"] == MULTICAST:
                handle_multicast(data)

            elif data["type"] == BROADCAST:
                handle_broadcast(data)

            elif data["type"] == FILE:
                handle_file(client_socket, data)

        except Exception as error:
            print(f"Client error: {error}")
            break

    # Cleanup saat client disconnect
    if client_socket in clients_username:
        disconnected_user = clients_username.pop(client_socket)
        remove_client(disconnected_user)
        print(f"{disconnected_user} disconnected")