#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from server.services.pc_build_agent import PCBuildAgent

print("\n" + "="*70)
print("TESTING ALL DOMAINS WITH PCBuildAgent")
print("="*70)

domains_to_test = [
    ('gaming', 120000),
    ('video_editing', 150000),
    ('streaming', 120000),
    ('rendering', 250000),
    ('programming', 100000),
]

for domain, budget in domains_to_test:
    result = PCBuildAgent.generate_build(domain, budget)
    success = result['success']
    print(f"\n[{domain.upper()}] Budget: ₹{budget:,}")
    print(f"  Status: {'✓ SUCCESS' if success else '✗ FAILED'}")
    
    if success:
        parts = result['parts']
        part_count = len(parts)
        print(f"  Parts: {part_count}")
        for part_type in ['cpu', 'gpu', 'ram', 'motherboard', 'storage', 'psu', 'case', 'cooler']:
            if part_type in parts:
                print(f"    ✓ {part_type.upper()}")
            else:
                print(f"    ✗ {part_type.upper()} MISSING")
        print(f"  Total: ₹{result['total_with_buffer']:,}")
    else:
        print(f"  Message: {result.get('message', 'No message')}")

print("\n" + "="*70)
