from server.managers.client_manager import get_all_clients
from shared.protocol import create_message


def handle_broadcast(data):
    all_clients = get_all_clients()
    sender = data["sender"]

    response = create_message(
        msg_type="MESSAGE",
        sender=f"[BROADCAST] {sender}",
        message=data["message"]
    )

    sent_count = 0

    for username, client_socket in all_clients.items():
        # tidak kirim ke pengirim sendiri
        if username == sender:
            continue

        try:
            client_socket.send(response.encode())
            sent_count += 1
        except Exception as error:
            print(f"[BROADCAST] Gagal kirim ke {username}: {error}")

    print(f"[BROADCAST] Pesan dari {sender} dikirim ke {sent_count} client")
