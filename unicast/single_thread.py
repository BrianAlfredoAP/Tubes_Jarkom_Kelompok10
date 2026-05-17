def unicast_single(sender, target, message, clients):

    if target not in clients:

        print(f"[ERROR] {target} tidak ditemukan")
        return

    clients[target].send(
        f"[UNICAST] {sender}: {message}".encode()
    )