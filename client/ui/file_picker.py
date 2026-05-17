import os

DOWNLOAD_DIR = "storage/downloads"


def show_received_files():
    if not os.path.exists(DOWNLOAD_DIR):
        print("\nNo downloaded files found")
        return

    files = os.listdir(DOWNLOAD_DIR)

    if not files:
        print("\nNo downloaded files")
        return

    print("\n=== RECEIVED FILES ===")

    for i, file in enumerate(files, start=1):
        filepath = os.path.join(DOWNLOAD_DIR, file)

        size = os.path.getsize(filepath)

        print(f"{i}. {file} ({size} bytes)")