#!/usr/bin/env python3
"""Test manual builder flow and compatibility analysis"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_manual_flow():
    print("=" * 60)
    print("TESTING MANUAL BUILDER FLOW")
    print("=" * 60)
    
    # Test 1: Quick parts API
    print("\n1. Testing Quick Parts API for each domain:")
    domains = ['gaming', 'video_editing', 'streaming', 'rendering', 'programming']
    
    for domain in domains:
        try:
            response = requests.get(f"{BASE_URL}/api/quick-parts/by-domain/{domain}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✓ {domain.upper()}: {len(data)} components found")
                if data:
                    print(f"     - CPU: {data[0].get('name', 'N/A')}")
                    print(f"     - GPU: {data[1].get('name', 'N/A')}")
            else:
                print(f"   ✗ {domain.upper()}: Error {response.status_code}")
        except Exception as e:
            print(f"   ✗ {domain.upper()}: {str(e)}")
    
    # Test 2: Compatibility API
    print("\n2. Testing Compatibility Analysis:")
    test_builds = [
        {
            "name": "Compatible Gaming Build",
            "components": {
                "cpu": "Intel Core i7-13700K",
                "motherboard": "ASUS ROG STRIX Z790-E",
                "ram": "DDR5 32GB",
                "gpu": "RTX 4070",
                "psu": "850W"
            }
        },
        {
            "name": "Socket Mismatch",
            "components": {
                "cpu": "Intel Core i7-13700K",
                "motherboard": "ASUS ROG STRIX B450",
                "ram": "DDR4 16GB",
                "gpu": "RTX 3070",
                "psu": "650W"
            }
        },
        {
            "name": "PSU Insufficient",
            "components": {
                "cpu": "AMD Ryzen 7 7700X",
                "motherboard": "MSI MPG B650E",
                "ram": "DDR5 32GB",
                "gpu": "RTX 4090",
                "psu": "550W"
            }
        }
    ]
    
    for build in test_builds:
        try:
            response = requests.post(
                f"{BASE_URL}/api/builder/compatibility",
                json=build["components"],
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n   Build: {build['name']}")
                print(f"   Status: {'✓ PASS' if data.get('success') else '✗ FAIL'}")
                if data.get('issues'):
                    print(f"   Issues: {', '.join(data['issues'])}")
                if data.get('warnings'):
                    print(f"   Warnings: {', '.join(data['warnings'])}")
                if not data.get('issues') and not data.get('warnings'):
                    print("   Result: All components compatible!")
                print(f"   Score: {data.get('overall_score', 0)}/100")
            else:
                print(f"   ✗ Error {response.status_code}")
        except Exception as e:
            print(f"   ✗ {str(e)}")
    
    # Test 3: Test routes
    print("\n3. Testing Routes:")
    routes = [
        ("/", "Home"),
        ("/manual-domain-selection", "Domain Selection"),
        ("/manual-goal-input", "Goal Input"),
        ("/manual-builder", "Manual Builder")
    ]
    
    for route, name in routes:
        try:
            response = requests.get(f"{BASE_URL}{route}")
            status = "✓" if response.status_code == 200 else "✗"
            print(f"   {status} {name}: {response.status_code}")
        except Exception as e:
            print(f"   ✗ {name}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    test_manual_flow()
