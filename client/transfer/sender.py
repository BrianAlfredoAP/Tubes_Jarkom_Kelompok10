from shared.protocol import create_message, UNICAST, MULTICAST, BROADCAST
from shared.config import ENCODING


def send_message(client_socket, sender, target, message):
    data = create_message(
        msg_type=UNICAST,
        sender=sender,
        target=target,
        message=message
    )

    client_socket.send(data.encode(ENCODING))


def send_multicast(client_socket, sender, targets, message):
    """targets: list of username strings."""
    target_str = ",".join(targets)

    data = create_message(
        msg_type=MULTICAST,
        sender=sender,
        target=target_str,
        message=message
    )

    client_socket.send(data.encode(ENCODING))


def send_broadcast(client_socket, sender, message):
    data = create_message(
        msg_type=BROADCAST,
        sender=sender,
        target="ALL",
        message=message
    )

    client_socket.send(data.encode(ENCODING))
