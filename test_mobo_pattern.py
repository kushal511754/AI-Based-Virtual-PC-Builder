#!/usr/bin/env python
"""Test different motherboards in detail"""
import requests
import json

tests = [
    ('MSI B450 Tomahawk', 'motherboard'),
    ('MSI B850', 'motherboard'),
    ('MSI B850 EDGE WIFI', 'motherboard'),
    ('MSI MPG', 'motherboard'),
    ('MSI Z790', 'motherboard'),
    ('ASUS', 'motherboard'),
]

for query, comp_type in tests:
    resp = requests.post('http://127.0.0.1:5000/api/search/component', 
        json={'query': query, 'component_type': comp_type}, 
        timeout=10)
    data = resp.json()
    status = "✓" if data.get('success') else "✗"
    result = data.get('component', {}).get('name') if data.get('success') else data.get('error')
    print(f"{status} {query:30} -> {result}")
