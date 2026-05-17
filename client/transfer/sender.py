from shared.protocol import create_message, UNICAST
from shared.config import ENCODING


def send_message(client_socket, sender, target, message):
    data = create_message(
        msg_type=UNICAST,
        sender=sender,
        target=target,
        message=message
    )

    client_socket.send(data.encode(ENCODING))