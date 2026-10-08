#!/usr/bin/env python
"""Debug script to test quick add functionality."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from server.app import create_app
from server.services.part_service import PartService

# Test the backend
print("[TEST] Testing PartService...")

try:
    cpus = PartService.get_all_cpus()
    print(f"✓ CPUs loaded: {len(cpus)} found")
    if cpus:
        print(f"  Sample: {cpus[0]}")
except Exception as e:
    print(f"✗ Error loading CPUs: {e}")

try:
    gpus = PartService.get_all_gpus()
    print(f"✓ GPUs loaded: {len(gpus)} found")
except Exception as e:
    print(f"✗ Error loading GPUs: {e}")

try:
    print("\n[TEST] Creating Flask app...")
    app = create_app()
    
    # Test the API endpoints
    with app.test_client() as client:
        print("\n[TEST] Testing API endpoints...")
        
        # Test CPU endpoint
        response = client.get('/api/parts/cpu')
        print(f"GET /api/parts/cpu - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"  ✓ Returned {len(data) if isinstance(data, list) else '?'} items")
            if isinstance(data, list) and len(data) > 0:
                print(f"  Sample: {data[0]}")
        else:
            print(f"  ✗ Error: {response.get_json()}")
        
        # Test GPU endpoint
        response = client.get('/api/parts/gpu')
        print(f"GET /api/parts/gpu - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"  ✓ Returned {len(data) if isinstance(data, list) else '?'} items")
        else:
            print(f"  ✗ Error: {response.get_json()}")
            
        # Test global search
        response = client.get('/api/parts/search?q=cpu&limit=5')
        print(f"GET /api/parts/search - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"  ✓ Found {data.get('count', 0)} results")
        else:
            print(f"  ✗ Error: {response.get_json()}")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n[TEST] Complete!")
