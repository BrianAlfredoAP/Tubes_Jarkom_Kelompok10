def handle_message(data):
    sender = data.get("sender")
    message = data.get("message")

    print(f"\n[{sender}] {message}")