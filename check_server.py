import requests

SERVERS = [
    "NA-PVE-Extinction5859",
]

URL = "https://cdn2.arkdedicated.com/servers/asa/officialserverlist.json"

try:
    response = requests.get(URL, timeout=30)
    response.raise_for_status()
    server_list = response.json()

    online_names = {
        str(server.get("Name", "")).lower()
        for server in server_list
    }

    for server_name in SERVERS:
        if server_name.lower() in online_names:
            print(f"{server_name} ONLINE")
        else:
            print(f"{server_name} OFFLINE")

except Exception as error:
    print(f"No se pudo consultar la lista: {error}")
    raise
