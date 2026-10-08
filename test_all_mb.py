#!/usr/bin/env python
"""Test to see if motherboard database is loading in running server"""
import requests
import json

# Let's test the database contents by searching for different motherboards
tests = [
    ('MSI B450 Tomahawk', 'motherboard'),
    ('MSI B450 Tomahawk (AM4)', 'motherboard'),
    ('ASUS TUF B550M-PLUS', 'motherboard'),
    ('AMD Ryzen 7 5800X3D', 'cpu'),
]

for query, comp_type in tests:
    resp = requests.post('http://127.0.0.1:5000/api/search/component', 
        json={'query': query, 'component_type': comp_type}, 
        timeout=10)
    data = resp.json()
    status = "✓" if data.get('success') else "✗"
    print(f"{status} {comp_type:15} {query:40} -> {data.get('component', {}).get('name') if data.get('success') else data.get('error')}")
