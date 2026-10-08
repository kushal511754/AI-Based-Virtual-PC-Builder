#!/usr/bin/env python
"""Test ML API endpoints via HTTP requests."""
import requests
import json
import time

BASE_URL = 'http://127.0.0.1:5000/api/ml'
TIMEOUT = 15

print("\n" + "="*70)
print("🧪 TESTING ML API ENDPOINTS (HTTP)")
print("="*70)

# Test 1: Health check
print("\n1️⃣ Testing Health Check...")
try:
    response = requests.get(f'{BASE_URL}/health', timeout=TIMEOUT)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Status: {data.get('status', 'unknown')}")
        print(f"   ✅ Response time: {response.elapsed.total_seconds():.3f}s")
    else:
        print(f"   ❌ Status {response.status_code}: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Game classification
print("\n2️⃣ Testing Game Classification (Naive Bayes)...")
try:
    payload = {'game_name': 'Cyberpunk 2077', 'aaa_status': True, 'release_year': 2020}
    response = requests.post(f'{BASE_URL}/classify-game-requirements', json=payload, timeout=TIMEOUT)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ Classification: {data.get('classification', 'N/A')}")
            print(f"   ✅ Confidence: {data.get('confidence', 0):.2%}")
            print(f"   ✅ Response time: {response.elapsed.total_seconds():.3f}s")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown')}")
    else:
        print(f"   ❌ Status {response.status_code}: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Price prediction
print("\n3️⃣ Testing Price Prediction (Ensemble Model)...")
try:
    payload = {'component': 'cpu', 'cores': 6, 'clock_speed': 3.2}
    response = requests.post(f'{BASE_URL}/predict-component-price', json=payload, timeout=TIMEOUT)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ Predicted Price: ₹{data.get('predicted_price', 0):,.0f}")
            print(f"   ✅ Response time: {response.elapsed.total_seconds():.3f}s")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown')}")
    else:
        print(f"   ❌ Status {response.status_code}: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Build cost prediction
print("\n4️⃣ Testing Build Cost Prediction...")
try:
    payload = {
        'cpu': {'cores': 6, 'clock_speed': 3.2},
        'gpu': {'vram_gb': 6, 'memory_bandwidth': 384},
        'ram': {'capacity_gb': 16, 'speed_mhz': 3600},
        'storage': {'capacity_gb': 512, 'type': 'ssd'}
    }
    response = requests.post(f'{BASE_URL}/predict-build-cost', json=payload, timeout=TIMEOUT)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ Total Build Cost: ₹{data.get('total_cost', 0):,.0f}")
            print(f"   ✅ Response time: {response.elapsed.total_seconds():.3f}s")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown')}")
    else:
        print(f"   ❌ Status {response.status_code}: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Build recommendation
print("\n5️⃣ Testing Build Recommendation (K-means Clustering)...")
try:
    payload = {'domain': 'gaming', 'budget_inr': 100000}
    response = requests.post(f'{BASE_URL}/recommend-build', json=payload, timeout=TIMEOUT)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ Recommended Tier: {data.get('tier', 'N/A')}")
            print(f"   ✅ Response time: {response.elapsed.total_seconds():.3f}s")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown')}")
    else:
        print(f"   ❌ Status {response.status_code}: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*70)
print("✅ API Testing Complete!")
print("="*70 + "\n")
