import subprocess
import time
import requests
import sys

# Start Flask server
print("Starting Flask server...")
flask_proc = subprocess.Popen(
    [sys.executable, "run.py"],
    cwd=r"c:\Users\LEENOVO\Desktop\projectk",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for Flask to start
print("Waiting for Flask to initialize...")
time.sleep(5)

# Test endpoints
base_url = "http://127.0.0.1:5000/api/ml"
endpoints = [
    ("health", "GET", None),
    ("classify-game-requirements", "POST", {"game_name": "Cyberpunk 2077"}),
    ("predict-component-price", "POST", {"component": "cpu", "cores": 6, "clock_speed": 3.2}),
]

print("\n" + "="*70)
print("TESTING ML ENDPOINTS")
print("="*70)

for endpoint, method, data in endpoints:
    url = f"{base_url}/{endpoint}"
    try:
        if method == "GET":
            resp = requests.get(url, timeout=5)
        else:
            resp = requests.post(url, json=data, timeout=5)
        
        status = "✅" if resp.status_code == 200 else "❌"
        print(f"{status} {method} /{endpoint}: {resp.status_code}")
        if resp.status_code == 200:
            print(f"   Response: {resp.json()}")
    except Exception as e:
        print(f"❌ {method} /{endpoint}: {e}")

# Kill Flask
flask_proc.terminate()
print("\n" + "="*70)
