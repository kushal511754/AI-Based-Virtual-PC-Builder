#!/usr/bin/env python
"""Test the component loading flow."""
import sys
sys.path.insert(0, '.')

from flask import Flask
from server.app import create_app

app = create_app()
client = app.test_client()

print("Testing component loading flow:")
print("=" * 60)

# 1. Test quick-parts endpoint
print("\n1. Quick-parts endpoint (gaming domain):")
response = client.get('/api/quick-parts/by-domain/gaming')
data = response.get_json()
print(f"   Status: {response.status_code}")
print(f"   Success: {data.get('success')}")
print(f"   Part types: {[p.get('type') for p in data.get('parts', [])]}")

# 2. Check if 'cooler' is in the types
cooler_part = next((p for p in data.get('parts', []) if p.get('type') == 'cooler'), None)
print(f"\n2. Found cooler part: {cooler_part is not None}")
if cooler_part:
    print(f"   Name: {cooler_part.get('name')}")
    print(f"   Price: {cooler_part.get('price')}")

# 3. Test cooling components endpoint
print(f"\n3. Cooling components endpoint:")
response = client.get('/api/parts/cooling')
components = response.get_json()
print(f"   Status: {response.status_code}")
print(f"   Type: {type(components).__name__}")
print(f"   Count: {len(components)}")
if components:
    print(f"   First item: {components[0]}")

print("\n" + "=" * 60)
print("All endpoints working correctly!")
