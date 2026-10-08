#!/usr/bin/env python
"""Check what quick parts returns."""
import sys
sys.path.insert(0, '.')

from flask import Flask
from server.app import create_app

app = create_app()
client = app.test_client()

# Test quick parts endpoint
response = client.get('/api/quick-parts/by-domain/gaming')
print('Status:', response.status_code)
data = response.get_json()
print('Response keys:', list(data.keys()) if isinstance(data, dict) else 'Not a dict')

if data and isinstance(data, dict) and 'parts' in data:
    print(f'Number of parts: {len(data["parts"])}')
    for part in data['parts']:
        part_type = part.get('type')
        part_name = part.get('name')
        print(f"  Type: '{part_type}' | Name: {part_name}")
