import requests
import json

# Test video_editing domain with ₹75,000
response = requests.post('http://127.0.0.1:5000/api/ai-build', json={
    'domain': 'video_editing',
    'budget': 75000,
    'game_name': 'Adobe Premiere'
})

result = response.json()
print('Status:', response.status_code)
print('Success:', result.get('success'))
print('Message:', result.get('message'))
print()
print('Parts:')
if result.get('suggested_parts'):
    for part, data in result['suggested_parts'].items():
        if data:
            print(f"  {part}: {data.get('name')} - Rs. {data.get('price_inr')}")
        else:
            print(f"  {part}: Not selected")
print()
print('Total Price:', result.get('total_price', 'N/A'), 'INR')
print('Compatibility:', result.get('compatibility', {}))
