#!/usr/bin/env python3
import requests
import json

url = 'http://localhost:5000/api/ai/suggest-build'
data = {
    'domain': 'gaming',
    'game_name': 'Cyberpunk 2077',
    'budget': 2000
}

response = requests.post(url, json=data)
result = response.json()

print("Full API Response JSON:")
print("=" * 60)
print(json.dumps(result, indent=2))
print()
print("=" * 60)
print("Motherboard in suggested_parts:")
print(json.dumps(result.get('suggested_parts', {}).get('motherboard'), indent=2))
