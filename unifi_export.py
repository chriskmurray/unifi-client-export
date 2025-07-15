import requests
import csv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === CONFIG ===
controller_url = "https://10.0.0.1"  # Replace with your controller IP or hostname
api_token = "K3htnYFPWNt-J6r0Wb1iMpK5P_gK1XVI"  # Replace with your actual API key
output_file = "unifi_clients.csv"

# === SETUP SESSION ===
session = requests.Session()
session.verify = False  # Allow self-signed SSL
session.headers.update({
    "X-API-KEY": api_token,
    "Accept": "application/json"
})

# === GET SITES LIST ===
sites_url = f"{controller_url}/proxy/network/integration/v1/sites"
sites_resp = session.get(sites_url)

if sites_resp.status_code != 200:
    print("Failed to fetch sites:", sites_resp.text)
    exit(1)

sites_raw = sites_resp.json()
sites = sites_raw.get("data", [])
if not sites:
    print("No sites found.")
    exit(1)

site_id = sites[0]["id"]
site_name = sites[0]["name"]
print(f"Using site '{site_name}' with ID: {site_id}")

# === GET CLIENTS FOR SITE ===
clients_url = f"{controller_url}/proxy/network/integration/v1/sites/{site_id}/clients?limit=100"
clients_resp = session.get(clients_url)

if clients_resp.status_code != 200:
    print("Failed to fetch clients:", clients_resp.text)
    exit(1)

clients = clients_resp.json().get("data", [])

# Optional: Uncomment below to debug clients JSON output
# import json
# print("Clients response:")
# print(json.dumps(clients, indent=2))

# === EXPORT CSV ===
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    # Header for NetBox import
    writer.writerow([
        "name", "device_type", "device_role", "site", "status", "manufacturer", "serial", "asset_tag", "comments"
    ])
    for client in clients:
        name = client.get("name", "")
        # Simple mapping example: treat wired/wireless as device roles
        device_role = "wired" if client.get("type", "").lower() == "wired" else "wireless"
        device_type = "Client Device"
        site = site_name
        status = "active"
        manufacturer = "Unknown"
        serial = ""
        asset_tag = ""
        comments = f"MAC: {client.get('macAddress', '')}, IP: {client.get('ipAddress', '')}"
        
        writer.writerow([
            name, device_type, device_role, site, status, manufacturer, serial, asset_tag, comments
        ])

print(f"Exported {len(clients)} clients to {output_file}")

# === OPTIONAL: MAC Vendor Lookup ===
# You could add a function here to lookup vendor info from the MAC address,
# then add that to your CSV rows as an extra column.
# Example libraries: 'mac_vendor_lookup' or 'manuf' Python package.
