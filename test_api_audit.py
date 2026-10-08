#!/usr/bin/env python
"""Test API endpoints."""
import requests

r = requests.get('http://127.0.0.1:5000/api/parts/cpu')
if r.status_code == 200:
    data = r.json()
    print(f'Total CPUs: {len(data)}')
    print('First CPU:')
    cpu = data[0]
    for key, val in cpu.items():
        print(f'  {key}: {val}')
else:
    print(f'Error: {r.status_code}')
