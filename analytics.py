import json
import os
import uuid
import datetime
from filelock import FileLock

ANALYTICS_FILE = "analytics.json"
LOCK_FILE = "analytics.lock"


def _ensure_file():
    """Create analytics file if missing."""
    if not os.path.exists(ANALYTICS_FILE):
        with open(ANALYTICS_FILE, "w") as f:
            json.dump({"visits": []}, f)


def log_visit(extra=None):
    """
    Log a single visit.
    `extra` can be a dict of additional metadata (e.g., location).
    """
    _ensure_file()

    session_id = str(uuid.uuid4())
    timestamp = datetime.datetime.utcnow().isoformat()

    entry = {
        "session_id": session_id,
        "timestamp": timestamp,
    }

    if isinstance(extra, dict):
        entry.update(extra)

    with FileLock(LOCK_FILE):
        with open(ANALYTICS_FILE, "r") as f:
            data = json.load(f)

        data["visits"].append(entry)

        with open(ANALYTICS_FILE, "w") as f:
            json.dump(data, f, indent=2)


def load_visits():
    """Return visits as a list of dicts."""
    _ensure_file()
    with open(ANALYTICS_FILE, "r") as f:
        data = json.load(f)
    return data["visits"]
