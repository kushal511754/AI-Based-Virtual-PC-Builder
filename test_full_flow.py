#!/usr/bin/env python
"""Direct test of the API flow"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from server.services.realtime_component_fetcher import RealtimeComponentFetcher

print("="*60)
print("TEST 1: Direct fetcher call")
print("="*60)

fetcher = RealtimeComponentFetcher()
result = fetcher.search_component("MSI B450 Tomahawk (AM4)", "motherboard")

print(f"Success: {result.get('success')}")
print(f"Error: {result.get('error')}")
if result.get('success'):
    comp = result['component']
    print(f"Component: {comp['name']}")
    print(f"Price INR: {comp['price_inr']}")

print("\n" + "="*60)
print("TEST 2: Via Flask test client")
print("="*60)

from server.app import create_app
import json

app = create_app()

with app.test_client() as client:
    resp = client.post('/api/search/component', 
        json={'query': 'MSI B450 Tomahawk (AM4)', 'component_type': 'motherboard'},
        content_type='application/json')
    
    print(f"Status: {resp.status_code}")
    data = resp.get_json()
    print(f"Success: {data.get('success')}")
    print(f"Error: {data.get('error')}")
    if data.get('success'):
        print(f"Component: {data['component']['name']}")
        print(f"Price INR: {data['component']['price_inr']}")

print("\n" + "="*60)
print("All tests completed")
print("="*60)
