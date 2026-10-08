#!/usr/bin/env python3
"""Test the compatibility engine with various component combinations."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from server.services.compatibility_engine import CompatibilityEngine
from server.utils.db import get_db_connection, dict_from_row

def test_compatibility():
    """Test compatibility checking"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get some test components
    cursor.execute("SELECT id, name, socket_type FROM cpu LIMIT 2")
    cpus = [dict_from_row(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT id, name, socket_type FROM motherboard LIMIT 2")
    motherboards = [dict_from_row(row) for row in cursor.fetchall()]
    
    print("Testing Compatibility Engine\n" + "="*50)
    
    if not cpus or not motherboards:
        print("No test data available")
        conn.close()
        return
    
    cpu1 = cpus[0]
    cpu2 = cpus[1] if len(cpus) > 1 else cpu1
    mb1 = motherboards[0]
    mb2 = motherboards[1] if len(motherboards) > 1 else mb1
    
    print(f"\nCPU 1: {cpu1['name']} (Socket: {cpu1['socket_type']})")
    print(f"CPU 2: {cpu2['name']} (Socket: {cpu2['socket_type']})")
    print(f"MB 1: {mb1['name']} (Socket: {mb1['socket_type']})")
    print(f"MB 2: {mb2['name']} (Socket: {mb2['socket_type']})")
    
    engine = CompatibilityEngine()
    
    # Test 1: CPU1 + MB1 (check if compatible)
    print(f"\n\nTest 1: {cpu1['name']} + {mb1['name']}")
    print("-" * 50)
    result = engine.validate_build(
        cpu_id=cpu1['id'],
        motherboard_id=mb1['id'],
        gpu_id=None,
        psu_id=None,
        case_id=None,
        ram_id=None,
        cooling_id=None
    )
    print(f"Compatible: {result['compatible']}")
    print(f"Errors: {result['errors']}")
    print(f"Warnings: {result['warnings']}")
    
    # Test 2: Try to force incompatibility (if we have different sockets)
    if cpu1['socket_type'] != mb2['socket_type']:
        print(f"\n\nTest 2: {cpu1['name']} + {mb2['name']} (DIFFERENT SOCKETS)")
        print("-" * 50)
        result = engine.validate_build(
            cpu_id=cpu1['id'],
            motherboard_id=mb2['id'],
            gpu_id=None,
            psu_id=None,
            case_id=None,
            ram_id=None,
            cooling_id=None
        )
        print(f"Compatible: {result['compatible']}")
        print(f"Errors: {result['errors']}")
        print(f"Warnings: {result['warnings']}")
    else:
        print(f"\n\nTest 2: Skipped (both motherboards have same socket type)")
    
    conn.close()

if __name__ == '__main__':
    test_compatibility()
