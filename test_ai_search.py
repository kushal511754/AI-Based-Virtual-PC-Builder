#!/usr/bin/env python3
"""Test the AI component search API."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from server.services.ai_component_search import AIComponentSearch

# Test the AI search
search = AIComponentSearch()

# Test 1: Search for CPU
print("Test 1: Searching for 'AMD Ryzen 7 5800X3D'")
print("=" * 60)
result = search.search_component("AMD Ryzen 7 5800X3D", "cpu")
print(f"Success: {result.get('success')}")
if result.get('success'):
    comp = result['component']
    print(f"Name: {comp.get('name')}")
    print(f"Socket: {comp.get('socket_type')}")
    print(f"Cores: {comp.get('cores')}")
    print(f"Price: ${comp.get('price')}")
else:
    print(f"Error: {result.get('error')}")

# Test 2: Search for GPU
print("\n\nTest 2: Searching for 'NVIDIA RTX 4070'")
print("=" * 60)
result = search.search_component("NVIDIA RTX 4070", "gpu")
print(f"Success: {result.get('success')}")
if result.get('success'):
    comp = result['component']
    print(f"Name: {comp.get('name')}")
    print(f"VRAM: {comp.get('vram_gb')}GB {comp.get('vram_type')}")
    print(f"Power Draw: {comp.get('power_draw')}W")
    print(f"Price: ${comp.get('price')}")
else:
    print(f"Error: {result.get('error')}")

# Test 3: Search for Motherboard
print("\n\nTest 3: Searching for 'MSI B550 Tomahawk'")
print("=" * 60)
result = search.search_component("MSI B550 Tomahawk", "motherboard")
print(f"Success: {result.get('success')}")
if result.get('success'):
    comp = result['component']
    print(f"Name: {comp.get('name')}")
    print(f"Socket: {comp.get('socket_type')}")
    print(f"Form Factor: {comp.get('form_factor')}")
    print(f"Price: ${comp.get('price')}")
else:
    print(f"Error: {result.get('error')}")
