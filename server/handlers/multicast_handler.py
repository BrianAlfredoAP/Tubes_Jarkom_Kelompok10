from server.managers.client_manager import get_client
from shared.protocol import create_message


def handle_multicast(data):
    # target berisi daftar username dipisahkan koma, misal: "user1,user2"
    targets = [t.strip() for t in data["target"].split(",") if t.strip()]

    response = create_message(
        msg_type="MESSAGE",
        sender=data["sender"],
        message=data["message"]
    )

    sent_count = 0
    failed = []

    for target in targets:
        target_socket = get_client(target)

        if target_socket:
            try:
                target_socket.send(response.encode())
                sent_count += 1
            except Exception as error:
                print(f"[MULTICAST] Gagal kirim ke {target}: {error}")
                failed.append(target)
        else:
            print(f"[MULTICAST] Target {target} tidak ditemukan")
            failed.append(target)

    print(f"[MULTICAST] Pesan dari {data['sender']} dikirim ke {sent_count}/{len(targets)} target")

    if failed:
        print(f"[MULTICAST] Gagal: {', '.join(failed)}")
