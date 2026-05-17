def multicast_message(
    sender,
    targets,
    message,
    clients
):

    for target in targets:

        target = target.strip()

        if target in clients:

            clients[target].send(
                f"[MULTICAST] {sender}: {message}".encode()
            )