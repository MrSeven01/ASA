import json
import os
from pathlib import Path

import requests

SERVERS = [
    "NA-PVE-Extinction5859",
]

SERVER_LIST_URL = (
    "https://cdn2.arkdedicated.com/servers/asa/"
    "officialserverlist.json"
)

STATE_FILE = Path("server_states.json")
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")


def send_discord(message):
    if not WEBHOOK_URL:
        raise RuntimeError("No se encontró DISCORD_WEBHOOK")

    response = requests.post(
        WEBHOOK_URL,
        json={
            "content": message,
            "allowed_mentions": {"parse": []},
        },
        timeout=20,
    )
    response.raise_for_status()


def load_previous_states():
    if not STATE_FILE.exists():
        return {}

    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


response = requests.get(SERVER_LIST_URL, timeout=30)
response.raise_for_status()
server_list = response.json()

online_names = {
    str(server.get("Name", "")).lower()
    for server in server_list
}

previous_states = load_previous_states()
current_states = {}

for server_name in SERVERS:
    is_online = server_name.lower() in online_names
    new_status = "online" if is_online else "offline"
    old_status = previous_states.get(server_name)

    current_states[server_name] = new_status

    if old_status is None:
        emoji = "🟢" if is_online else "🔴"
        send_discord(
            f"{emoji} Server **{server_name}** is currently "
            f"**{new_status.upper()}**!"
        )

    elif old_status != new_status:
        if is_online:
            send_discord(f"🟢 Server **{server_name}** went up!")
        else:
            send_discord(f"🔴 Server **{server_name}** went down!")

    print(f"{server_name}: {new_status.upper()}")

STATE_FILE.write_text(
    json.dumps(current_states, indent=2),
    encoding="utf-8",
    )
