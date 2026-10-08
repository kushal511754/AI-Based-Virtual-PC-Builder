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

print("Response Status:", response.status_code)
print("\nFull Response:")
print(json.dumps(result, indent=2, default=str))

if result.get('success'):
    print("\n\nSuggested Parts:")
    for part_type, part_data in result.get('suggested_parts', {}).items():
        if part_data:
            print(f"\n{part_type.upper()}:")
            print(f"  Name: {part_data.get('name')}")
            print(f"  Price: ${part_data.get('price')}")
        else:
            print(f"\n{part_type.upper()}: NOT FOUND")
