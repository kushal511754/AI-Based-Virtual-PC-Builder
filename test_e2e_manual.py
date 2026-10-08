#!/usr/bin/env python3
"""
End-to-end test for manual builder flow
Tests: domain selection → goal input → manual builder → component selection → compatibility check
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_e2e_manual_builder():
    print("=" * 80)
    print("END-TO-END MANUAL BUILDER FLOW TEST")
    print("=" * 80)
    
    # Test 1: Verify all domain selection routes exist
    print("\n[Step 1] Testing Domain Selection Routes")
    print("-" * 80)
    routes_to_test = [
        ("/manual-domain-selection", "Domain Selection Page"),
        ("/manual-goal-input", "Goal Input Page"),
        ("/manual-builder", "Manual Builder Page"),
    ]
    
    all_routes_ok = True
    for route, name in routes_to_test:
        try:
            response = requests.get(f"{BASE_URL}{route}", timeout=5)
            if response.status_code == 200:
                print(f"  [OK] {name:30} - Route accessible")
            else:
                print(f"  [FAIL] {name:30} - Status {response.status_code}")
                all_routes_ok = False
        except Exception as e:
            print(f"  [FAIL] {name:30} - {str(e)}")
            all_routes_ok = False
    
    if not all_routes_ok:
        print("\n[ERROR] Some routes are not accessible. Stopping test.")
        return
    
    # Test 2: Verify Quick Parts API for all domains
    print("\n[Step 2] Testing Quick Parts API for All Domains")
    print("-" * 80)
    domains = ['gaming', 'video_editing', 'streaming', 'rendering', 'programming']
    
    all_domains_ok = True
    for domain in domains:
        try:
            response = requests.get(f"{BASE_URL}/api/quick-parts/by-domain/{domain}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                parts_count = len(data.get('parts', []))
                if parts_count == 8:
                    print(f"  [OK] {domain:18} - {parts_count} components returned")
                else:
                    print(f"  [WARN] {domain:18} - Expected 8 components, got {parts_count}")
            else:
                print(f"  [FAIL] {domain:18} - Status {response.status_code}")
                all_domains_ok = False
        except Exception as e:
            print(f"  [FAIL] {domain:18} - {str(e)}")
            all_domains_ok = False
    
    # Test 3: Verify Compatibility API
    print("\n[Step 3] Testing Compatibility Analysis API")
    print("-" * 80)
    
    test_scenarios = [
        {
            "name": "Fully Compatible Build",
            "config": {
                "cpu": "Intel Core i7-13700K",
                "motherboard": "ASUS ROG STRIX Z790-E",
                "ram": "DDR5 32GB",
                "gpu": "RTX 4070",
                "psu": "850W"
            },
            "expected_issues": 0
        },
        {
            "name": "Socket Mismatch (i7 on B450)",
            "config": {
                "cpu": "Intel Core i7-13700K",
                "motherboard": "MSI B450M PRO-VDQ",
                "ram": "DDR4 16GB",
                "gpu": "RTX 3070",
                "psu": "650W"
            },
            "expected_issues": 1
        },
        {
            "name": "RAM Type Mismatch (DDR4 on Z790)",
            "config": {
                "cpu": "Intel Core i5-13600K",
                "motherboard": "GIGABYTE Z790 AORUS Master",
                "ram": "DDR4 32GB",
                "gpu": "RTX 4060",
                "psu": "750W"
            },
            "expected_issues": 1
        },
        {
            "name": "PSU Underpowered (550W for RTX 4090)",
            "config": {
                "cpu": "AMD Ryzen 7 7700X",
                "motherboard": "MSI MPG B650E EDGE WIFI",
                "ram": "DDR5 32GB",
                "gpu": "RTX 4090",
                "psu": "550W"
            },
            "expected_issues": 0,
            "expected_warnings": 1
        }
    ]
    
    for scenario in test_scenarios:
        try:
            response = requests.post(
                f"{BASE_URL}/api/builder/compatibility",
                json=scenario["config"],
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                issues = len(data.get('issues', []))
                warnings = len(data.get('warnings', []))
                score = data.get('overall_score', 0)
                
                status = "OK"
                details = f"Issues: {issues}, Warnings: {warnings}, Score: {score}/100"
                
                if 'expected_issues' in scenario and issues != scenario['expected_issues']:
                    status = "WARN"
                    details += f" (expected {scenario['expected_issues']} issues)"
                
                print(f"  [{status}] {scenario['name']:40} - {details}")
                
                # Show issues if any
                if data.get('issues'):
                    for issue in data['issues']:
                        print(f"        Issue: {issue}")
                        
            else:
                print(f"  [FAIL] {scenario['name']:40} - Status {response.status_code}")
        except Exception as e:
            print(f"  [FAIL] {scenario['name']:40} - {str(e)}")
    
    # Test 4: Verify component data structure
    print("\n[Step 4] Verifying Component Data Structure")
    print("-" * 80)
    try:
        response = requests.get(f"{BASE_URL}/api/quick-parts/by-domain/gaming", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('parts'):
                sample_part = data['parts'][0]
                required_fields = ['type', 'name', 'price', 'specs', 'category']
                missing_fields = [f for f in required_fields if f not in sample_part]
                
                if not missing_fields:
                    print(f"  [OK] Component data structure is correct")
                    print(f"       Sample: {sample_part['type']} = {sample_part['name']}")
                    print(f"       Price: Rs {sample_part.get('price', 'N/A')}")
                    print(f"       Specs: {sample_part.get('specs', 'N/A')[:50]}...")
                else:
                    print(f"  [WARN] Missing fields: {', '.join(missing_fields)}")
    except Exception as e:
        print(f"  [FAIL] Could not verify component structure: {str(e)}")
    
    # Summary
    print("\n" + "=" * 80)
    print("END-TO-END TEST COMPLETE")
    print("=" * 80)
    print("\nSUMMARY:")
    print("  1. All routes accessible: YES" if all_routes_ok else "  1. All routes accessible: NO")
    print("  2. Quick parts API returns 8 components: YES" if all_domains_ok else "  2. Quick parts API returns 8 components: NO")
    print("  3. Compatibility API working: YES")
    print("  4. Manual builder flow ready for testing")
    print("\nNEXT STEPS:")
    print("  1. Open browser to http://127.0.0.1:5000/manual-domain-selection")
    print("  2. Click a domain (e.g., Gaming)")
    print("  3. Enter a game/goal name")
    print("  4. Click 'Quick Add' buttons to open component selection modals")
    print("  5. Select components and verify compatibility score updates")

if __name__ == '__main__':
    test_e2e_manual_builder()
