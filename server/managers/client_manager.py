clients = {}


def add_client(username, client_socket):
    clients[username] = client_socket


def remove_client(username):
    if username in clients:
        del clients[username]


def get_client(username):
    return clients.get(username)