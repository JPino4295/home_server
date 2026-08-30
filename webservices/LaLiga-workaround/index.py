import os
import time
import requests

# Config from environment variables
CF_API_TOKEN = os.getenv("CF_API_TOKEN")
CF_ZONE_ID = os.getenv("CF_ZONE_ID")
RECORD_NAMES = [r.strip() for r in os.getenv("RECORD_NAMES", "").split(",") if r.strip()]
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "180")) # 3 minutes

HAYAHORA_API = "https://hayahora.futbol/estado/data.json"
CF_API_BASE = f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records"

headers = {
    "Authorization": f"Bearer {CF_API_TOKEN}",
    "Content-Type": "application/json"
}

def is_match_active():
    try:
        response = requests.get(HAYAHORA_API, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # If the API flags active blocks, football/ISP censorship is ongoing
            return data.get("blocked", False) or data.get("estado", "") == "BLOQUEADO"
    except Exception as e:
        print(f"[!] Error checking match status: {e}")
    return False

def get_record_id(record_name):
    try:
        res = requests.get(f"{CF_API_BASE}?name={record_name}", headers=headers).json()
        if res.get("success") and res.get("result"):
            return res["result"][0]["id"], res["result"][0]["proxied"]
    except Exception as e:
        print(f"[!] Error fetching record {record_name}: {e}")
    return None, None

def set_proxy_status(record_name, target_proxied_state):
    rec_id, current_proxied = get_record_id(record_name)
    if not rec_id:
        print(f"[!] Could not find record for {record_name}")
        return

    if current_proxied == target_proxied_state:
        print(f"[*] {record_name} is already set to proxied={target_proxied_state}. No change needed.")
        return

    payload = {"proxied": target_proxied_state}
    res = requests.patch(f"{CF_API_BASE}/{rec_id}", headers=headers, json=payload).json()
    if res.get("success"):
        state_str = "PROXIED (Orange)" if target_proxied_state else "DNS ONLY (Grey)"
        print(f"[SUCCESS] Updated {record_name} to {state_str}")
    else:
        print(f"[!] Failed to update {record_name}: {res.get('errors')}")

def main():
    print("[INIT] Cloudflare Match-Day Toggle Monitor started...")
    while True:
        match_active = is_match_active()
        # If match is active -> proxy should be OFF (false). If no match -> proxy ON (true).
        desired_proxy_state = not match_active 
        
        status_msg = "MATCH IN PROGRESS (Bypassing Proxy)" if match_active else "NO MATCH (Proxy Active)"
        print(f"[STATUS] {status_msg}")

        for record in RECORD_NAMES:
            set_proxy_status(record, desired_proxy_state)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
