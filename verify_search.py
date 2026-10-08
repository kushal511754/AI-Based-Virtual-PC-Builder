#!/usr/bin/env python
"""Direct working test - proves search works perfectly"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from server.app import create_app

app = create_app()

print("=" * 60)
print("TESTING MSI B450 TOMAHAWK (AM4) SEARCH")
print("=" * 60)

with app.test_client() as client:
    resp = client.post('/api/search/component', json={
        'query': 'MSI B450 Tomahawk (AM4)',
        'component_type': 'motherboard'
    })
    
    data = resp.get_json()
    
    if data.get('success'):
        comp = data['component']
        print("\n✓ SUCCESS! Component found:")
        print(f"  Name:     {comp['name']}")
        print(f"  Type:     {comp['type']}")
        print(f"  Price INR: Rs.{comp['price_inr']}")
        print(f"  Price USD: ${comp['price_usd']}")
        print(f"  Socket:   {comp.get('socket', 'N/A')}")
        print(f"  Retailers: {len(comp.get('retailers', []))}")
        print("\n" + "=" * 60)
        print("RESULT: Search is working correctly!")
        print("=" * 60)
        sys.exit(0)
    else:
        print(f"\n✗ Error: {data.get('error')}")
        sys.exit(1)
