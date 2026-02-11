import os
import time
import subprocess
import urllib.request
import json

# Configuration
GATEWAY_URL = "http://127.0.0.1:18789"
OPENCLAW_PATH = "/Users/sheshnarayaniyer/.nvm/versions/node/v22.16.0/bin/openclaw"
TELEGRAM_ID = "1371522080"

def is_gateway_up():
    try:
        # Check health endpoint
        with urllib.request.urlopen(f"{GATEWAY_URL}/status", timeout=5) as response:
            return response.getcode() == 200
    except Exception as e:
        return False

def restart_gateway():
    print(f"[{time.ctime()}] Gateway is down. Triggering restart...")
    try:
        # Use absolute path and force flag if necessary
        subprocess.run([OPENCLAW_PATH, "gateway", "restart"], check=True, capture_output=True)
        # Give it time to initialize
        time.sleep(20)
    except subprocess.CalledProcessError as e:
        print(f"Error restarting gateway: {e.stderr.decode()}")

def notify_user():
    print(f"[{time.ctime()}] Sending notification...")
    msg = "🛡️ Watchdog: OpenClaw Gateway was detected as DOWN and has been auto-restarted. Field resonance restored."
    try:
        subprocess.run([
            OPENCLAW_PATH, "message", "send",
            "--channel", "telegram",
            "--target", TELEGRAM_ID,
            "--message", msg
        ], check=True, capture_output=True)
    except Exception as e:
        print(f"Failed to send notification: {e}")

if __name__ == "__main__":
    if not is_gateway_up():
        restart_gateway()
        # Verify it came back up before notifying
        if is_gateway_up():
            notify_user()
        else:
            print("Restart attempted but gateway is still not responding.")
