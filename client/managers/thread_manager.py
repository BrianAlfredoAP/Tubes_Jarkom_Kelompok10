import threading

from client.transfer.receiver import receive_data


def start_receiver_thread(client_socket):
    receiver_thread = threading.Thread(
        target=receive_data,
        args=(client_socket,),
        daemon=True
    )

    receiver_thread.start()