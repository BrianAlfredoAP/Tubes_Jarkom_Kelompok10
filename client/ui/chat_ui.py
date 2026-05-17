def show_welcome():
    print("""
=================================
      SIMPLE CHAT APPLICATION
=================================
""")


def show_help():
    print("""
Commands:
1. Chat User
2. Upload File
3. View Received Files
4. Help
5. Exit
""")


def show_chat_header(username):
    print(f"\n===== Chat with {username} =====")


def show_incoming_message(sender, message):
    print(f"\n[{sender}] {message}")


def show_success(message):
    print(f"\n[SUCCESS] {message}")


def show_error(message):
    print(f"\n[ERROR] {message}")