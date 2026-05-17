import json

MESSAGE = "MESSAGE"
UNICAST = "UNICAST"
MULTICAST = "MULTICAST"
BROADCAST = "BROADCAST"
FILE = "FILE"
SUCCESS = "SUCCESS"
ERROR = "ERROR"


def create_message(msg_type, sender=None, target=None, message=None, filename=None, filesize=None):
    data = {
        "type": msg_type,
        "sender": sender,
        "target": target,
        "message": message,
        "filename": filename,
        "filesize": filesize,
    }

    return json.dumps(data)


def parse_message(raw_data):
    return json.loads(raw_data)