#!/usr/bin/env python3
from server.services.pc_build_agent import PCBuildAgent

# Test streaming domain
print("=" * 60)
print("Testing Streaming Domain Configuration")
print("=" * 60)

result = PCBuildAgent.generate_build('streaming', 50000)
print('\nTest 1: Streaming with ₹50,000 budget')
success = result["success"]
print(f'Success: {success}')
if success:
    parts = result["parts"]
    print(f'Parts found: {list(parts.keys())}')
    for part_name, part_data in parts.items():
        price = part_data["price_inr"]
        name = part_data["name"]
        print(f'  {part_name}: {name} - ₹{price}')
else:
    msg = result.get("message", "No message")
    print(f'Message: {msg}')

print("\n" + "=" * 60)
result2 = PCBuildAgent.generate_build('streaming', 120000)
print('Test 2: Streaming with ₹120,000 budget')
success2 = result2["success"]
print(f'Success: {success2}')
if success2:
    total = result2["total_with_buffer"]
    subtotal = result2["subtotal"]
    print(f'Subtotal: ₹{subtotal}')
    print(f'Total with buffer: ₹{total}')
    parts2 = result2["parts"]
    print(f'Parts: {list(parts2.keys())}')
else:
    msg = result2.get("message", "No message")
    print(f'Message: {msg}')

print("\n" + "=" * 60)
print("Testing with ₹50,000 (Budget Validation Check)")
result3 = PCBuildAgent.generate_build('streaming', 50000)
print(f'Success: {result3["success"]}')
if not result3["success"]:
    print(f'Expected: Budget too low')
    print(f'Actual: {result3.get("message", "No message")}')
    print(f'Min Required: ₹{result3.get("min_required", "Unknown")}')
print("=" * 60)
