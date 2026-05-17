import socket
import threading
from transfer.file_transfer import send_file

HOST = "127.0.0.1"
PORT = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = input("Username: ")
client.send(username.encode())


def receive_message():

    while True:

        try:

            message = client.recv(4096).decode()

            if not message:
                break

            print(f"\n{message}")
            print("Pilih menu: ", end="", flush=True)

        except Exception as e:

            print(f"[ERROR] {e}")
            break


receive_thread = threading.Thread(
    target=receive_message
)

receive_thread.start()


while True:

    print("""
========= MENU =========

1. Unicast Single Thread
2. Unicast Multithread
3. Multicast
4. Broadcast
5. Send File
6. Exit

========================
""")

    choice = input("Pilih menu: ")

    # UNICAST SINGLE
    if choice == "1":

        target = input("Target username: ")
        message = input("Pesan: ")

        command = f"/unicast {target} {message}"

        client.send(command.encode())

    # UNICAST MULTITHREAD
    elif choice == "2":

        target = input("Target username: ")
        message = input("Pesan: ")

        command = f"/unicast {target} {message}"

        client.send(command.encode())

    # MULTICAST
    elif choice == "3":

        targets = input(
            "Target usernames (pisahkan koma): "
        )

        message = input("Pesan: ")

        command = f"/multicast {targets} {message}"

        client.send(command.encode())

    # BROADCAST
    elif choice == "4":

        message = input("Pesan broadcast: ")

        command = f"/broadcast {message}"

        client.send(command.encode())

    # SEND FILE
    elif choice == "5":

        filepath = input("Path file: ")

        send_file(client, filepath)

    # EXIT
    elif choice == "6":

        client.close()
        break

    else:
        print("[ERROR] Menu tidak valid")