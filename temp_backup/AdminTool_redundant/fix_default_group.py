import requests
import sys

# Configuration from admin_gui.py
API_URL = "https://backend.aidg168.uk/api/v1"
TOKEN = "admin-secret-token"
HEADERS = {"x-admin-token": TOKEN}

def fix_group():
    print(f"Connecting to {API_URL}...")
    
    # 1. List groups
    try:
        resp = requests.get(f"{API_URL}/admin/groups", headers=HEADERS)
        resp.raise_for_status()
        groups = resp.json()
    except Exception as e:
        print(f"Error listing groups: {e}")
        print("Please check your network connection or server status.")
        return

    print(f"Found {len(groups)} groups.")
    
    target_group = None
    default_exists = False
    
    for g in groups:
        print(f"  - ID: {g['id']}, Name: {g['name']}, Comment: {g.get('comment')}")
        if g['name'] == '默认':
            target_group = g
        if g['name'] == 'default':
            default_exists = True

    if default_exists:
        print("\n[OK] Group 'default' already exists.")
        if target_group:
             print("Warning: Group '默认' also exists. Please verify which one you want to keep.")
        else:
             print("Everything looks good.")
        return

    if target_group:
        print(f"\nFound group '默认' (ID: {target_group['id']}). Renaming to 'default'...")
        try:
            url = f"{API_URL}/admin/groups/{target_group['id']}"
            # The API expects JSON body with fields to update
            resp = requests.put(url, json={"name": "default"}, headers=HEADERS)
            resp.raise_for_status()
            print("Success! Group renamed to 'default'.")
        except Exception as e:
            print(f"Error renaming group: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Server response: {e.response.text}")
    else:
        print("\nGroup '默认' not found and 'default' does not exist.")
        print("Creating 'default' group...")
        try:
            url = f"{API_URL}/admin/groups"
            payload = {"name": "default", "comment": "Default User Group"}
            resp = requests.post(url, json=payload, headers=HEADERS)
            resp.raise_for_status()
            print("Success! Group 'default' created.")
        except Exception as e:
            print(f"Error creating group: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Server response: {e.response.text}")

if __name__ == "__main__":
    fix_group()
