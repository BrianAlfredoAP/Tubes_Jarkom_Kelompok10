from shared.config import BUFFER_SIZE, ENCODING
from shared.protocol import parse_message

from client.handlers.message_handler import handle_message
from client.handlers.response_handler import handle_response
from client.handlers.file_handler import handle_file


def receive_data(client_socket):
    while True:
        try:
            raw_data = client_socket.recv(BUFFER_SIZE)

            if not raw_data:
                break

            # decode metadata JSON only
            data = parse_message(raw_data.decode(ENCODING))

            message_type = data["type"]

            if message_type == "MESSAGE":
                handle_message(data)

            elif message_type == "RESPONSE":
                handle_response(data)

            elif message_type == "FILE":
                handle_file(client_socket, data)

        except Exception as error:
            print(f"Receive Error: {error}")
            break