from client.managers.connection_manager import connect_server
from client.managers.thread_manager import start_receiver_thread
from client.managers.command_manager import process_command

from client.utils.file_utils import show_received_files

from client.ui.chat_ui import (
    show_help,
    show_welcome
)


def show_menu():
    print("\n===== MENU =====")
    print("1. Chat User")
    print("2. Upload File")
    print("3. View Received Files")
    print("4. Help")
    print("5. Exit")


def main():
    show_welcome()

    client_socket = connect_server()

    username = input("Enter username: ")
    client_socket.send(username.encode())

    start_receiver_thread(client_socket)

    current_target = None

    while True:
        show_menu()

        choice = input("Choose: ")

        if choice == "1":
            target = input("Target username: ")

            current_target = target

            message = input(f"[{target}] Message: ")

            command = message

            current_target = process_command(
                client_socket,
                username,
                command,
                current_target
            )

        elif choice == "2":
            filepath = input("File path: ")

            command = f"/upload {filepath}"

            current_target = process_command(
                client_socket,
                username,
                command,
                current_target
            )

        elif choice == "3":
            show_received_files()

        elif choice == "4":
            show_help()

        elif choice == "5":
            process_command(
                client_socket,
                username,
                "/exit",
                current_target
            )
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()