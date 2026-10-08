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

print("\n" + "="*70)
print("TESTING ML ENDPOINTS")
print("="*70)

try:
    resp = requests.get(f"{base_url}/health", timeout=5)
    print(f"Health Check: {resp.status_code}")
    print(f"Response: {resp.json()}")
except Exception as e:
    print(f"Health Check Error: {e}")

try:
    resp = requests.post(f"{base_url}/classify-game-requirements", 
                         json={"game_name": "Cyberpunk 2077"}, timeout=5)
    print(f"\nGame Classification: {resp.status_code}")
    print(f"Response: {resp.json()}")
except Exception as e:
    print(f"Game Classification Error: {e}")

try:
    resp = requests.post(f"{base_url}/predict-component-price",
                         json={"component": "cpu", "cores": 6, "clock_speed": 3.2}, timeout=5)
    print(f"\nPrice Prediction: {resp.status_code}")
    print(f"Response: {resp.json()}")
except Exception as e:
    print(f"Price Prediction Error: {e}")

# Kill Flask
print("\n" + "="*70)
print("Shutting down Flask server...")
flask_proc.terminate()
flask_proc.wait(timeout=5)
print("Done!")
