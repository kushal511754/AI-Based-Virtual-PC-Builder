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

if result.get('success'):
    parts = result['suggested_parts']
    print('Keys in suggested_parts:', list(parts.keys()))
    print()
    
    motherboard = parts.get('motherboard')
    print('Motherboard value:', motherboard)
    print('Motherboard type:', type(motherboard))
    
    if motherboard:
        print('Motherboard is not None/null')
        print('Motherboard keys:', list(motherboard.keys()) if isinstance(motherboard, dict) else 'NOT A DICT')
    else:
        print('Motherboard is None/null!')
else:
    print('API returned success=False')
    print('Result:', result)
