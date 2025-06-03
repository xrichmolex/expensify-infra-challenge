#!/usr/bin/env python3
import requests
import sys

def load_server_list(file_path):
    """Reads a list of servers from a file"""
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"UNKNOWN - Error reading server list: {e}")
        sys.exit(3)

def is_server_online(url):
    """Returns True if server responds with HTTP 200, else False."""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def check_servers(servers):
    """Checks each server and returns a list of the ones that are down."""
    down = [url for url in servers if not is_server_online(url)]
    return down

def main(file_path):
    servers = load_server_list(file_path)
    if not servers:
        print("UNKNOWN - No servers defined in the list.")
        sys.exit(3)

    down = check_servers(servers)

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
    main(sys.argv[1])