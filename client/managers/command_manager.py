from client.transfer.sender import send_message, send_multicast, send_broadcast
from client.transfer.file_transfer import upload_file, upload_file_multicast, upload_file_broadcast


def process_command(client_socket, username, command, current_target):

    # SET TARGET CHAT
    if command.startswith("/to"):
        parts = command.split(" ", 1)

        if len(parts) < 2:
            print("Usage: /to <username>")
            return current_target

        current_target = parts[1]

        print(f"Now chatting with {current_target}")

        return current_target

    # FILE UPLOAD (unicast)
    elif command.startswith("/upload"):
        parts = command.split(" ", 1)

        if len(parts) < 2:
            print("Usage: /upload <filepath>")
            return current_target

        if not current_target:
            print("Set target first using /to")
            return current_target

        filepath = parts[1]

        upload_file(
            client_socket,
            username,
            current_target,
            filepath
        )

        return current_target

    # MULTICAST PESAN: /mcast user1,user2 <pesan>
    elif command.startswith("/mcast"):
        parts = command.split(" ", 2)

        if len(parts) < 3:
            print("Usage: /mcast <user1,user2,...> <pesan>")
            return current_target

        targets = [t.strip() for t in parts[1].split(",") if t.strip()]
        message = parts[2]

        send_multicast(client_socket, username, targets, message)

        print(f"[MULTICAST] Pesan dikirim ke: {', '.join(targets)}")

        return current_target

    # MULTICAST FILE: /mcastfile user1,user2 <filepath>
    elif command.startswith("/mcastfile"):
        parts = command.split(" ", 2)

        if len(parts) < 3:
            print("Usage: /mcastfile <user1,user2,...> <filepath>")
            return current_target

        targets = [t.strip() for t in parts[1].split(",") if t.strip()]
        filepath = parts[2]

        upload_file_multicast(client_socket, username, targets, filepath)

        return current_target

    # BROADCAST PESAN: /broadcast <pesan>
    elif command.startswith("/broadcast"):
        parts = command.split(" ", 1)

        if len(parts) < 2:
            print("Usage: /broadcast <pesan>")
            return current_target

        message = parts[1]

        send_broadcast(client_socket, username, message)

        print(f"[BROADCAST] Pesan dikirim ke semua client")

        return current_target

    # BROADCAST FILE: /bcastfile <filepath>
    elif command.startswith("/bcastfile"):
        parts = command.split(" ", 1)

        if len(parts) < 2:
            print("Usage: /bcastfile <filepath>")
            return current_target

        filepath = parts[1]

        upload_file_broadcast(client_socket, username, filepath)

        return current_target

    # EXIT
    elif command == "/exit":
        client_socket.close()
        exit()

    # HELP
    elif command == "/help":
        print("""
Commands:
  [UNICAST]
    /to <username>           - Set target chat
    /upload <filepath>       - Kirim file ke target saat ini

  [MULTICAST]
    /mcast <u1,u2> <pesan>   - Kirim pesan ke beberapa user
    /mcastfile <u1,u2> <fp>  - Kirim file ke beberapa user

  [BROADCAST]
    /broadcast <pesan>       - Kirim pesan ke semua client
    /bcastfile <filepath>    - Kirim file ke semua client

    /exit                    - Keluar
        """)
        return current_target

    # NORMAL CHAT MESSAGE (unicast)
    else:
        if not current_target:
            print("Set target first using /to")
            return current_target

        send_message(
            client_socket,
            username,
            current_target,
            command
        )

        return current_target
