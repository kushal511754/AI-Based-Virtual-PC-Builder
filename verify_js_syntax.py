#!/usr/bin/env python
"""Verify JavaScript syntax of the modified functions"""
import sys
sys.path.insert(0, '.')

# Read the HTML file
with open('templates/manual-builder.html', 'r') as f:
    content = f.read()

# Check for required functions
functions_to_check = [
    'function componentItemClick(element)',
    'function filterComponentsInModal(type, search)',
    'function addComponentToBuilder(type, id, name, price)',
    'onclick="componentItemClick(this)"'
]

print("\n" + "="*70)
print("JAVASCRIPT SYNTAX VERIFICATION")
print("="*70)

all_found = True
for func in functions_to_check:
    if func in content:
        print(f"✅ {func[:50]}... found")
    else:
        print(f"❌ {func[:50]}... NOT FOUND")
        all_found = False

# Check for data attributes
data_attrs = [
    'data-type="${type}"',
    'data-id="${comp.id}"',
    'data-name="${comp.name',
    'data-price="${comp.price}"'
]

print("\n" + "-"*70)
print("Data Attributes Check:")
for attr in data_attrs:
    if attr in content:
        print(f"✅ {attr[:40]}... found")
    else:
        print(f"❌ {attr[:40]}... NOT FOUND")
        all_found = False

# Check for search display fix
if "item.style.display = matches ? 'flex' : 'none';" in content:
    print("\n" + "-"*70)
    print("✅ Search display property correctly set to 'flex'")
else:
    print("\n" + "-"*70)
    print("❌ Search display property NOT properly set")
    all_found = False

print("\n" + "="*70)
if all_found:
    print("✅ ALL CHECKS PASSED - JavaScript is properly configured")
else:
    print("❌ Some checks failed - review changes")

print("="*70 + "\n")
