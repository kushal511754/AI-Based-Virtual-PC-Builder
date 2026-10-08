#!/usr/bin/env python3
"""
Test script to verify streaming domain parts are selected correctly
"""
import sys
sys.path.insert(0, '.')

from server.services.pc_build_agent import PCBuildAgent

def test_streaming_domain():
    """Test streaming domain with various budgets"""
    
    print("\n" + "="*70)
    print("STREAMING DOMAIN - PARTS SELECTION TEST")
    print("="*70)
    
    # Test case: Streaming with ₹50,000 (below minimum)
    print("\n[TEST 1] Budget: ₹50,000 (Below Minimum)")
    result = PCBuildAgent.generate_build('streaming', 50000)
    print(f"  Result: {'✗ FAIL' if result['success'] else '✓ EXPECTED (Budget too low)'}")
    print(f"  Message: {result.get('message', 'N/A')}")
    
    # Test case: Streaming with ₹100,000
    print("\n[TEST 2] Budget: ₹100,000 (Mid-range)")
    result = PCBuildAgent.generate_build('streaming', 100000)
    if result['success']:
        print(f"  ✓ Success - Parts selected:")
        parts = result['parts']
        for category in ['cpu', 'gpu', 'ram', 'motherboard', 'storage', 'psu', 'case', 'cooler']:
            if category in parts:
                part = parts[category]
                print(f"    - {category.upper():15} ✓ {part['name'][:40]:40} ₹{part['price_inr']:,}")
            else:
                print(f"    - {category.upper():15} ✗ MISSING!")
        print(f"  Total (with buffer): ₹{result['total_with_buffer']:,}")
    else:
        print(f"  ✗ FAILED: {result.get('message', 'Unknown error')}")
    
    # Test case: Streaming with ₹150,000
    print("\n[TEST 3] Budget: ₹150,000 (Premium)")
    result = PCBuildAgent.generate_build('streaming', 150000)
    if result['success']:
        print(f"  ✓ Success - Parts selected:")
        parts = result['parts']
        for category in ['cpu', 'gpu', 'ram', 'motherboard', 'storage', 'psu', 'case', 'cooler']:
            if category in parts:
                part = parts[category]
                print(f"    - {category.upper():15} ✓ {part['name'][:40]:40} ₹{part['price_inr']:,}")
            else:
                print(f"    - {category.upper():15} ✗ MISSING!")
        print(f"  Total (with buffer): ₹{result['total_with_buffer']:,}")
    else:
        print(f"  ✗ FAILED: {result.get('message', 'Unknown error')}")
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)

if __name__ == '__main__':
    test_streaming_domain()
