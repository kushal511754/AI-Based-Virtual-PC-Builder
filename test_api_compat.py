#!/usr/bin/env python3
"""Test API endpoint directly"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from server.services.compatibility_engine import CompatibilityEngine

engine = CompatibilityEngine()

# Test incompatible combo: CPU 1 (LGA1700) + Motherboard 3 (AM5)
print("Testing CPU 1 (LGA1700) + Motherboard 3 (AM5) - SHOULD FAIL")
print("=" * 60)

result = engine.validate_build(
    cpu_id=1,
    motherboard_id=3,
    gpu_id=None,
    psu_id=None,
    case_id=None,
    ram_id=None,
    cooling_id=None
)

print(f"Compatible: {result['compatible']}")
print(f"Errors: {result['errors']}")
print(f"Warnings: {result['warnings']}")

print("\n\nTesting CPU 1 (LGA1700) + Motherboard 1 (LGA1700) - SHOULD PASS")
print("=" * 60)

result2 = engine.validate_build(
    cpu_id=1,
    motherboard_id=1,
    gpu_id=None,
    psu_id=None,
    case_id=None,
    ram_id=None,
    cooling_id=None
)

print(f"Compatible: {result2['compatible']}")
print(f"Errors: {result2['errors']}")
print(f"Warnings: {result2['warnings']}")
