def broadcast_message(
    sender,
    message,
    clients
):

    print(f"[BROADCAST] {sender}: {message}")

    for username, client_socket in clients.items():

        if username != sender:

            client_socket.send(
                f"[BROADCAST] {sender}: {message}".encode()
            )