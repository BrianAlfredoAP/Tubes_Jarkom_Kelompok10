import threading

from server.handlers.client_handler import handle_client


def start_client_thread(client_socket):
    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket,),
        daemon=True
    )

    client_thread.start()