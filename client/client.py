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
    print("--- A. Unicast ---")
    print("1. Chat User (Unicast)")
    print("2. Upload File (Unicast)")
    print("--- B. Multicast ---")
    print("3. Chat Multicast (A->B,C)")
    print("4. Upload File Multicast (A->B,C)")
    print("--- C. Broadcast ---")
    print("5. Chat Broadcast (A->Semua)")
    print("6. Upload File Broadcast (A->Semua)")
    print("-----------------")
    print("7. View Received Files")
    print("8. Help")
    print("9. Exit")


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

        # ===== UNICAST =====
        if choice == "1":
            target = input("Target username: ")
            current_target = target
            message = input(f"[{target}] Message: ")
            current_target = process_command(
                client_socket, username, message, current_target
            )

        elif choice == "2":
            target = input("Target username: ")
            current_target = target
            filepath = input("File path: ")
            command = f"/upload {filepath}"
            current_target = process_command(
                client_socket, username, command, current_target
            )

        # ===== MULTICAST =====
        elif choice == "3":
            targets = input("Target usernames (pisahkan koma, cth: user1,user2): ")
            message = input(f"[MULTICAST->{targets}] Message: ")
            command = f"/mcast {targets} {message}"
            current_target = process_command(
                client_socket, username, command, current_target
            )

        elif choice == "4":
            targets = input("Target usernames (pisahkan koma, cth: user1,user2): ")
            filepath = input("File path: ")
            command = f"/mcastfile {targets} {filepath}"
            current_target = process_command(
                client_socket, username, command, current_target
            )

        # ===== BROADCAST =====
        elif choice == "5":
            message = input("[BROADCAST->Semua] Message: ")
            command = f"/broadcast {message}"
            current_target = process_command(
                client_socket, username, command, current_target
            )

        elif choice == "6":
            filepath = input("File path: ")
            command = f"/bcastfile {filepath}"
            current_target = process_command(
                client_socket, username, command, current_target
            )

        # ===== UTILITAS =====
        elif choice == "7":
            show_received_files()

        elif choice == "8":
            show_help()

        elif choice == "9":
            process_command(
                client_socket, username, "/exit", current_target
            )
            break

        else:
            print("Pilihan tidak valid")


if __name__ == "__main__":
    main()
