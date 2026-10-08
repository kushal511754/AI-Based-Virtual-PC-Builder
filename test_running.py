import requests, json
r = requests.post('http://127.0.0.1:5000/api/search/component', 
    json={'query': 'MSI B450 Tomahawk (AM4)', 'component_type': 'motherboard'}, timeout=10)
print(f'Status: {r.status_code}')
data = r.json()
print(f'Success: {data.get("success")}')
if not data.get('success'):
    print(f'Error: {data.get("error")}')
else:
    print(f'Component: {data["component"]["name"]}')
    print(f'Price INR: {data["component"]["price_inr"]}')
