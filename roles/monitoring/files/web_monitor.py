#!/usr/bin/env python3
import requests
import sys

def check_servers(file_path):
    try:
        with open(file_path, 'r') as f:
            servers = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"UNKNOWN - Error reading server list: {e}")
        sys.exit(3)

    down = []
    for url in servers:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                down.append(url)
        except Exception:
            down.append(url)

    if len(down) == len(servers):
        print(f"CRITICAL - All servers are down: {', '.join(down)}")
        sys.exit(2)
    elif down:
        print(f"WARNING - Some servers are down: {', '.join(down)}")
        sys.exit(1)
    else:
        print("OK - All servers are up")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: web_monitor.py <server_list_file>")
        sys.exit(3)
    check_servers(sys.argv[1])