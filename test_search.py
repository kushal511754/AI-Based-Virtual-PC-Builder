#!/usr/bin/env python
"""Test the search API"""
import requests
import json
import time

# Give server a moment to start
time.sleep(3)

url = 'http://127.0.0.1:5000/api/search/component'
payload = {'query': 'MSI B450 Tomahawk (AM4)', 'component_type': 'motherboard'}

try:
    r = requests.post(url, json=payload, timeout=15)
    result = r.json()
    if result.get('success'):
        comp = result.get('component', {})
        print('SUCCESS! Found Component:')
        print('Name:', comp.get('name'))
        print('Price INR:', comp.get('price_inr'))
        print('Price USD:', comp.get('price_usd'))
        print('Socket:', comp.get('socket'))
    else:
        print('Error:', result.get('error'))
except Exception as e:
    print('Exception:', str(e))
