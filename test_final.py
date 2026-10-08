#!/usr/bin/env python
"""Direct test of the search API without running server"""
from server.app import create_app
import json

app = create_app()

with app.test_client() as client:
    print("=" * 70)
    print("TEST: MSI B450 Tomahawk (AM4) Search")
    print("=" * 70)
    
    resp = client.post('/api/search/component', 
        json={'query': 'MSI B450 Tomahawk (AM4)', 'component_type': 'motherboard'},
        content_type='application/json')
    
    print(f"Status: {resp.status_code}")
    data = resp.get_json()
    print(f"Success: {data.get('success')}")
    
    if data.get('success'):
        comp = data['component']
        print(f"\n✓ COMPONENT FOUND!")
        print(f"  Name: {comp['name']}")
        print(f"  Type: {comp['type']}")
        print(f"  Socket: {comp.get('socket')}")
        print(f"  Price INR: ₹{comp.get('price_inr'):,}")
        print(f"  Price USD: ${comp.get('price_usd'):.2f}")
        print(f"  Retailers: {len(comp.get('retailers', []))} stores")
        for retail in comp.get('retailers', []):
            print(f"    - {retail['name']}: {retail['url']}")
    else:
        print(f"\n✗ ERROR: {data.get('error')}")
