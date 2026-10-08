import requests
import json

# First, test just the realtime endpoint directly
resp = requests.post('http://127.0.0.1:5000/api/search/component', 
    json={'query': 'AMD Ryzen 7 5800X3D', 'component_type': 'cpu'}, 
    timeout=10)
    
print("TEST 1: CPU search")
print(f"Status: {resp.status_code}")
data = resp.json()
print(f"Success: {data.get('success')}")
print(f"Component: {data.get('component', {}).get('name') if data.get('success') else 'N/A'}")
print()

# Now test the motherboard search
resp2 = requests.post('http://127.0.0.1:5000/api/search/component', 
    json={'query': 'MSI B450 Tomahawk (AM4)', 'component_type': 'motherboard'}, 
    timeout=10)
    
print("TEST 2: Motherboard search")
print(f"Status: {resp2.status_code}")
data2 = resp2.json()
print(f"Success: {data2.get('success')}")
print(f"Error: {data2.get('error')}")
print()

# Test with auto-detection (no component type)
resp3 = requests.post('http://127.0.0.1:5000/api/search/component', 
    json={'query': 'MSI B450 Tomahawk (AM4)'}, 
    timeout=10)
    
print("TEST 3: Motherboard search with auto-detection")
print(f"Status: {resp3.status_code}")
data3 = resp3.json()
print(f"Success: {data3.get('success')}")
print(f"Error: {data3.get('error')}")
