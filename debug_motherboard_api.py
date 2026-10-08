#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/LEENOVO/Desktop/projectk')

from server.services.ai_build_service import AIBuildService
import json

# Test the AI service
result = AIBuildService.get_ai_suggestion('gaming', 'Cyberpunk 2077', 2000)

print("=" * 60)
print("API Result:")
print("=" * 60)
print(f"Success: {result['success']}")
print(f"Total Price: ${result['total_price']}")
print()

print("Suggested Parts:")
print("-" * 60)
for comp_type, component in result['suggested_parts'].items():
    if component:
        print(f"{comp_type.upper()}: {component.get('name', 'Unknown')} (${component.get('price', 0)})")
    else:
        print(f"{comp_type.upper()}: None (NOT FOUND)")

print()
print("=" * 60)
print("Motherboard Details:")
print("=" * 60)
if result['suggested_parts'].get('motherboard'):
    mb = result['suggested_parts']['motherboard']
    print(json.dumps(mb, indent=2, default=str))
else:
    print("Motherboard is None!")
