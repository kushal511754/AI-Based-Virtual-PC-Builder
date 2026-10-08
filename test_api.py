#!/usr/bin/env python
import time
import sys
time.sleep(2)

try:
    import requests
    print("Testing /api/builder/check endpoint...")
    r = requests.post('http://127.0.0.1:5000/api/builder/check', 
                      json={'cpu': 1, 'motherboard': 3},  
                      timeout=5)
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.json()}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# DELETE EVERYTHING BELOW
import requests
import json

BASE_URL = "http://localhost:5000"
API_URL = f"{BASE_URL}/api/ai"

print("\n" + "="*80)
print("GAME DATABASE API TEST EXAMPLES")
print("="*80)

print(f"\nServer: {BASE_URL}")
print(f"API Endpoint: {API_URL}/game-requirements")

# Example 1: Get game requirements for BGMI
print("\n" + "-"*80)
print("EXAMPLE 1: Get BGMI Requirements")
print("-"*80)

try:
    response = requests.get(
        f"{API_URL}/game-requirements",
        params={"game_name": "BGMI"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Request successful!")
        print(f"  Game: {result.get('game_name')}")
        print(f"  Type: {result.get('game_type')}")
        print(f"  Platforms: {', '.join(result.get('platforms', []))}")
        print(f"  Source: {result.get('source')}")
        print(f"\n  Minimum Specs:")
        min_specs = result.get('minimum', {})
        print(f"    - CPU: {min_specs.get('cpu_cores')} cores")
        print(f"    - GPU: {min_specs.get('gpu_vram')}GB VRAM")
        print(f"    - RAM: {min_specs.get('ram_gb')}GB")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.json())
except Exception as e:
    print(f"✗ Connection Error: {e}")
    print("  Make sure the server is running: python run.py")

# Example 2: Get Minecraft requirements
print("\n" + "-"*80)
print("EXAMPLE 2: Get Minecraft Requirements")
print("-"*80)

try:
    response = requests.get(
        f"{API_URL}/game-requirements",
        params={"game_name": "minecraft"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Request successful!")
        print(f"  Game: {result.get('game_name')}")
        print(f"  Type: {result.get('game_type')}")
        print(f"  Source: {result.get('source')}")
        print(f"\n  High-End Specs:")
        high_specs = result.get('high_end', {})
        print(f"    - CPU: {high_specs.get('cpu_cores')} cores ({high_specs.get('cpu_name')})")
        print(f"    - GPU: {high_specs.get('gpu_vram')}GB VRAM ({high_specs.get('gpu_name')})")
        print(f"    - RAM: {high_specs.get('ram_gb')}GB")
        print(f"\n  Estimated FPS:")
        for res, fps in result.get('estimated_fps', {}).items():
            print(f"    - {res}: {fps}")
    else:
        print(f"✗ Error: {response.status_code}")
except Exception as e:
    print(f"✗ Connection Error: {e}")

# Example 3: Get build recommendation for Fortnite with budget
print("\n" + "-"*80)
print("EXAMPLE 3: Get Build Recommendation (Fortnite, ₹60,000 budget)")
print("-"*80)

try:
    response = requests.post(
        f"{API_URL}/game-build-recommendation",
        json={
            "game_name": "Fortnite",
            "budget": 60000,
            "domain": "gaming"
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Request successful!")
        print(f"  Game: {result.get('game_name')}")
        print(f"  Budget: ₹{result.get('budget'):,}")
        print(f"  Build Tier: {result.get('build_recommendation', {}).get('build_tier').upper()}")
        
        build = result.get('build_recommendation', {})
        print(f"\n  Recommended Components (INR):")
        print(f"    - CPU: ₹{build.get('cpu_inr'):,}")
        print(f"    - GPU: ₹{build.get('gpu_inr'):,}")
        print(f"    - RAM: ₹{build.get('ram_inr'):,}")
        print(f"    - Storage: ₹{build.get('storage_inr'):,}")
        print(f"    - PSU: ₹{build.get('psu_inr'):,}")
        print(f"    - Case: ₹{build.get('case_inr'):,}")
        print(f"    - Cooling: ₹{build.get('cooling_inr'):,}")
        print(f"\n  Total Cost: ₹{build.get('total_inr'):,}")
        print(f"  Target: {build.get('target_fps')}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.json())
except Exception as e:
    print(f"✗ Connection Error: {e}")

# Example 4: Get Cyberpunk 2077 requirements with high budget
print("\n" + "-"*80)
print("EXAMPLE 4: High-Budget Build (Cyberpunk 2077, ₹150,000)")
print("-"*80)

try:
    response = requests.post(
        f"{API_URL}/game-build-recommendation",
        json={
            "game_name": "Cyberpunk 2077",
            "budget": 150000,
            "domain": "gaming"
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Request successful!")
        print(f"  Game: {result.get('game_name')}")
        print(f"  Budget: ₹{result.get('budget'):,}")
        print(f"  Build Tier: {result.get('build_recommendation', {}).get('build_tier').upper()}")
        
        build = result.get('build_recommendation', {})
        print(f"  Total Cost: ₹{build.get('total_inr'):,}")
        print(f"  Target: {build.get('target_fps')}")
    else:
        print(f"✗ Error: {response.status_code}")
except Exception as e:
    print(f"✗ Connection Error: {e}")

# Example 5: Search for a game not in database (fallback)
print("\n" + "-"*80)
print("EXAMPLE 5: Unknown Game (Fallback System)")
print("-"*80)

try:
    response = requests.get(
        f"{API_URL}/game-requirements",
        params={"game_name": "some_unknown_indie_game_2024"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Request successful!")
        print(f"  Game: {result.get('game_name')}")
        print(f"  Source: {result.get('source')} (automatic fallback)")
        print(f"  Notes: {result.get('notes')}")
        print(f"\n  Generated Specs:")
        print(f"    - Min RAM: {result.get('minimum', {}).get('ram_gb')}GB")
        print(f"    - Rec RAM: {result.get('recommended', {}).get('ram_gb')}GB")
        print(f"    - High RAM: {result.get('high_end', {}).get('ram_gb')}GB")
    else:
        print(f"✗ Error: {response.status_code}")
except Exception as e:
    print(f"✗ Connection Error: {e}")

# Example 6: Validate PC specs for a game
print("\n" + "-"*80)
print("EXAMPLE 6: Validate PC Specs for Game")
print("-"*80)

try:
    response = requests.post(
        f"{API_URL}/validate-pc-for-game",
        json={
            "game_name": "Cyberpunk 2077",
            "pc_specs": {
                "cpu_cores": 8,
                "gpu_vram": 6,
                "ram_gb": 16
            }
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Request successful!")
        print(f"  Game: {result.get('game_name')}")
        print(f"  Your PC: 8 cores, 6GB VRAM, 16GB RAM")
        print(f"  Can Run: {'YES ✓' if result.get('can_run') else 'NO ✗'}")
        print(f"  Performance: {result.get('performance_level', 'Standard')}")
    else:
        print(f"✗ Error: {response.status_code}")
except Exception as e:
    print(f"✗ Connection Error: {e}")

print("\n" + "="*80)
print("TESTING COMPLETE")
print("="*80)
print("\nUsage Guide:")
print("  1. GET /api/ai/game-requirements?game_name=BGMI")
print("     → Get hardware requirements for any game")
print("\n  2. POST /api/ai/game-build-recommendation")
print("     → Get full build with INR pricing and budget breakdown")
print("\n  3. POST /api/ai/validate-pc-for-game")
print("     → Check if your PC can run a game")
print("\n" + "="*80 + "\n")
