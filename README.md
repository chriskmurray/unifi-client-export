A work in progress, my first attempt at pulling network info via an API

# Unifi Client Export

Export connected client devices from a UniFi Controller and format them into a CSV compatible with [NetBox](https://github.com/netbox-community/netbox) device imports.

---
# Features

- Connects to UniFi Controller via API
- Exports wired and wireless clients
- Outputs CSV with NetBox-compatible headers
- Annotates MAC and IP address in comments
- Designed for homelab or production visibility

### Prerequisites

- Python 3.7+
- UniFi Controller with API token access
- `requests` library installed:
  ```bash
  pip install requests
