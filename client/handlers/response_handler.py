def handle_response(data):
    status = data.get("status")
    message = data.get("message")

    if status == "SUCCESS":
        print(f"[SUCCESS] {message}")

    elif status == "ERROR":
        print(f"[ERROR] {message}")

    else:
        print(f"[INFO] {message}")