from shared.config import BUFFER_SIZE, ENCODING
from shared.protocol import parse_message, UNICAST, FILE

from server.handlers.unicast_handler import handle_unicast
from server.handlers.file_handler import handle_file
from server.managers.client_manager import add_client

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

            elif data["type"] == FILE:
                handle_file(client_socket, data)

        except Exception as error:
            print(f"Client error: {error}")
            break