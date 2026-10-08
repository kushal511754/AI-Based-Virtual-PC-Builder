#!/usr/bin/env python
"""Direct test of parts API endpoints."""
import sys
sys.path.insert(0, '.')

from server.services.part_service import PartService
import json

print("="*60)
print("Direct PartService Test")
print("="*60)

try:
    print("\n1. Testing PartService.get_all_cooling()...")
    cooling = PartService.get_all_cooling()
    print(f"   Type: {type(cooling)}")
    print(f"   Count: {len(cooling)}")
    if cooling:
        sample = cooling[0]
        print(f"   Sample: {sample}")
        print(f"   Keys: {list(sample.keys()) if isinstance(sample, dict) else 'Not a dict'}")
    else:
        print("   NO RESULTS!")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Testing Flask endpoint directly...")
print("="*60)

from flask import Flask
from server.app import create_app

try:
    app = create_app()
    
    # Create test client
    client = app.test_client()
    
    print("\n2. Testing /api/parts/cooling endpoint...")
    response = client.get('/api/parts/cooling')
    print(f"   Status: {response.status_code}")
    print(f"   Response type: {type(response.json)}")
    data = response.get_json()
    print(f"   Response is list: {isinstance(data, list)}")
    print(f"   Response length: {len(data) if isinstance(data, list) else 'N/A'}")
    if isinstance(data, list) and data:
        print(f"   Sample: {data[0]}")
    print(f"   First 300 chars: {str(data)[:300]}")
        
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()
