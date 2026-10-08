#!/usr/bin/env python
"""Test the search API with test client"""
from server.app import create_app

app = create_app()

with app.test_client() as client:
    resp = client.post('/api/search/component', json={
        'query': 'MSI B450 Tomahawk (AM4)',
        'component_type': ''
    })
    
    data = resp.get_json()
    if data.get('success'):
        comp = data['component']
        print("=" * 50)
        print("SUCCESS! Found component:")
        print("=" * 50)
        print(f"Name:     {comp['name']}")
        print(f"Type:     {comp['type']}")
        print(f"Price:    Rs.{comp['price_inr']} / ${comp['price_usd']}")
        print(f"Socket:   {comp.get('socket')}")
        print(f"Retailers: {len(comp.get('retailers', []))}")
        print("=" * 50)
    else:
        print(f"ERROR: {data.get('error')}")
