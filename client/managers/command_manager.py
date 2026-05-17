from client.transfer.sender import send_message
from client.transfer.file_transfer import upload_file


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

    # FILE UPLOAD
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

    # EXIT
    elif command == "/exit":
        client_socket.close()
        exit()

    # HELP
    elif command == "/help":
        print("""
Commands:
/to <username>
/upload <filepath>
/exit
        """)
        return current_target

    # NORMAL CHAT MESSAGE
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