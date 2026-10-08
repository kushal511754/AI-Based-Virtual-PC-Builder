#!/usr/bin/env python3
"""
Test script to verify the complete AI PC Builder flow.
Simulates a user selecting a domain and getting AI suggestions.
"""

import requests
import json
import sys

BASE_URL = 'http://127.0.0.1:5000'

def test_complete_flow():
    """Test the complete AI builder flow."""
    
    print("\n" + "=" * 70)
    print("  AI PC BUILDER - COMPLETE FLOW TEST")
    print("=" * 70)
    
    # Test 1: Get domains
    print("\n[TEST 1] Getting available domains...")
    try:
        response = requests.get(f'{BASE_URL}/api/ai/domains', timeout=10)
        response.raise_for_status()
        domains_data = response.json()
        
        if not domains_data.get('success'):
            print("  FAILED: API returned success=False")
            return False
            
        domains = domains_data.get('domains', [])
        print(f"  PASSED: Found {len(domains)} domains")
        for d in domains:
            print(f"          - {d['name']} ({d['id']})")
    except Exception as e:
        print(f"  FAILED: {str(e)}")
        return False
    
    # Test 2: Test each domain with AI suggestions
    test_cases = [
        {'domain': 'video_editing', 'game_name': 'Adobe Premiere', 'budget': 75000, 'desc': 'Video Editing'},
        {'domain': 'gaming', 'game_name': 'Cyberpunk 2077', 'budget': 100000, 'desc': 'Gaming'},
        {'domain': 'programming', 'game_name': 'Visual Studio Code', 'budget': 60000, 'desc': 'Programming'},
        {'domain': 'rendering', 'game_name': 'Blender', 'budget': 200000, 'desc': 'Rendering'},
        {'domain': 'streaming', 'game_name': 'OBS', 'budget': 150000, 'desc': 'Streaming'},
    ]
    
    for i, test in enumerate(test_cases, 2):
        print(f"\n[TEST {i}] Getting AI suggestions for {test['desc']} with budget {test['budget']}...")
        try:
            payload = {
                'domain': test['domain'],
                'game_name': test['game_name'],
                'budget': test['budget']
            }
            response = requests.post(
                f'{BASE_URL}/api/ai/suggest-build',
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            suggestion = response.json()
            
            if not suggestion.get('success'):
                print(f"  FAILED: {suggestion.get('message', 'Unknown error')}")
                return False
            
            # Verify response structure
            required_fields = ['domain', 'budget', 'total_price', 'suggested_parts', 'compatibility']
            missing = [f for f in required_fields if f not in suggestion]
            
            if missing:
                print(f"  FAILED: Missing fields: {missing}")
                return False
            
            # Verify parts
            parts = suggestion.get('suggested_parts', {})
            parts_count = sum(1 for p in parts.values() if p is not None)
            
            print(f"  PASSED:")
            print(f"          - Domain: {suggestion['domain']}")
            print(f"          - Budget: {suggestion['budget']}")
            print(f"          - Total Price: {suggestion['total_price']}")
            print(f"          - Parts: {parts_count}/8 selected")
            print(f"          - Compatibility: {len(suggestion['compatibility'].get('errors', []))} errors, {len(suggestion['compatibility'].get('warnings', []))} warnings")
            
        except Exception as e:
            print(f"  FAILED: {str(e)}")
            return False
    
    # Test 3: Verify the flow completes successfully
    print("\n" + "=" * 70)
    print("  ALL TESTS PASSED - AI BUILDER IS WORKING CORRECTLY!")
    print("=" * 70 + "\n")
    return True

if __name__ == '__main__':
    success = test_complete_flow()
    sys.exit(0 if success else 1)
