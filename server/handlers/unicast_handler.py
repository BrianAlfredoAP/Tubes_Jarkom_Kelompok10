from server.managers.client_manager import get_client
from shared.protocol import create_message


def handle_unicast(data):
    target_socket = get_client(data["target"])

    if target_socket:

        response = create_message(
            msg_type="MESSAGE",
            sender=data["sender"],
            message=data["message"]
        )

        target_socket.send(response.encode())