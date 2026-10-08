#!/usr/bin/env python3
"""Test ML API endpoints quickly"""
import requests
import json
import time

BASE_URL = 'http://127.0.0.1:5000/api/ml'

print("🧪 Testing ML API Endpoints...")
print()

# Test 1: Game Classification
print("1️⃣ Testing Game Classification (Naive Bayes)...")
try:
    response = requests.post(
        f'{BASE_URL}/classify-game-requirements',
        json={'game_name': 'BGMI'},
        timeout=10
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Game: {data.get('game_name')}")
        print(f"   Classification: {data.get('classification')} (Confidence: {data.get('confidence')})")
    else:
        print(f"   ❌ Error: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# Test 2: Price Prediction
print("2️⃣ Testing Price Prediction (Ensemble Model)...")
try:
    response = requests.post(
        f'{BASE_URL}/predict-component-price',
        json={
            'component_type': 'cpu',
            'specs': {'cores': 8, 'ghz': 4.5, 'generation': 13}
        },
        timeout=10
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ CPU Price: Rs {data.get('predicted_price_inr'):,.0f}")
    else:
        print(f"   ❌ Error: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# Test 3: Build Recommendation
print("3️⃣ Testing Build Recommendation (K-means Clustering)...")
try:
    response = requests.post(
        f'{BASE_URL}/recommend-build',
        json={
            'domain': 'gaming',
            'budget_inr': 100000
        },
        timeout=10
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Tier: {data.get('tier')}")
        print(f"   Budget Utilization: {data.get('budget_utilization')}")
    else:
        print(f"   ❌ Error: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# Test 4: Health Check
print("4️⃣ Testing ML Health Check...")
try:
    response = requests.get(f'{BASE_URL}/health', timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Status: {data.get('status')}")
        services = ', '.join([f"{k}={v}" for k,v in data.get('ml_services', {}).items()])
        print(f"   Services: {services}")
    else:
        print(f"   ❌ Error: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()
print("✅ ML API Tests Complete!")
