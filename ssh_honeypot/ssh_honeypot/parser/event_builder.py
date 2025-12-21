import json
import time

LOG_FILE = "logs/ssh_events.jsonl"


def log_event(event_type, data):
    event = {
        "ts": time.time(),
        "type": event_type,
        **data
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")
