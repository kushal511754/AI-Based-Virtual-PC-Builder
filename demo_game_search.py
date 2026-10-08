#!/usr/bin/env python
"""
DEMO: Search Games and Get Results from Dataset
Shows how to use the 506-game database with examples
"""

from server.services.openai_game_analyzer import OpenAIGameAnalyzer

print("\n" + "="*70)
print("GAME DATABASE SEARCH & RESULTS DEMO")
print("="*70)

# Initialize analyzer (loads 506 games on startup)
analyzer = OpenAIGameAnalyzer()

print("\n✓ Database initialized with 506 games")
print("  - 6 core games (hardcoded)")
print("  - 500 Steam games (from dataset)")

# Example 1: Search for a core game
print("\n" + "-"*70)
print("EXAMPLE 1: Search for CORE GAME - BGMI")
print("-"*70)

result = analyzer.extract_game_requirements('bgmi')
print(f"\nGame: {result.get('game_name')}")
print(f"Type: {result.get('game_type')}")
print(f"Platforms: {', '.join(result.get('platforms', []))}")
print(f"Source: {result.get('source')}")
print(f"\nMINIMUM SPECS:")
min_specs = result.get('minimum', {})
print(f"  CPU: {min_specs.get('cpu_cores')} cores ({min_specs.get('cpu_name')})")
print(f"  GPU: {min_specs.get('gpu_vram')}GB VRAM ({min_specs.get('gpu_name')})")
print(f"  RAM: {min_specs.get('ram_gb')}GB")
print(f"  Storage: {min_specs.get('storage_gb')}GB")
print(f"  OS: {min_specs.get('os')}")
print(f"\nRECOMMENDED SPECS:")
rec_specs = result.get('recommended', {})
print(f"  CPU: {rec_specs.get('cpu_cores')} cores ({rec_specs.get('cpu_name')})")
print(f"  GPU: {rec_specs.get('gpu_vram')}GB VRAM ({rec_specs.get('gpu_name')})")
print(f"  RAM: {rec_specs.get('ram_gb')}GB")
print(f"  Storage: {rec_specs.get('storage_gb')}GB")
print(f"  OS: {rec_specs.get('os')}")

# Example 2: Search for another core game
print("\n" + "-"*70)
print("EXAMPLE 2: Search for CORE GAME - Minecraft")
print("-"*70)

result = analyzer.extract_game_requirements('minecraft')
print(f"\nGame: {result.get('game_name')}")
print(f"Type: {result.get('game_type')}")
print(f"Source: {result.get('source')}")
print(f"\nHIGH-END SPECS (for maximum performance):")
high_specs = result.get('high_end', {})
print(f"  CPU: {high_specs.get('cpu_cores')} cores ({high_specs.get('cpu_name')})")
print(f"  GPU: {high_specs.get('gpu_vram')}GB VRAM ({high_specs.get('gpu_name')})")
print(f"  RAM: {high_specs.get('ram_gb')}GB")
print(f"  Storage: {high_specs.get('storage_gb')}GB")
print(f"\nESTIMATED FPS (at recommended specs):")
for resolution, fps in result.get('estimated_fps', {}).items():
    print(f"  {resolution}: {fps}")

# Example 3: Build recommendation with INR budget
print("\n" + "-"*70)
print("EXAMPLE 3: Build Recommendation for Cyberpunk 2077 (Budget: ₹75,000)")
print("-"*70)

result = analyzer.get_game_and_build_recommendation('cyberpunk 2077', 75000)
print(f"\nGame: {result.get('game_name')}")
print(f"Budget: ₹{result.get('budget_inr'):,}")
print(f"Build Tier: {result.get('build_recommendation', {}).get('build_tier').upper()}")
print(f"\nRECOMMENDED COMPONENTS:")
build = result.get('build_recommendation', {})
print(f"  CPU: ₹{build.get('cpu_inr'):,}")
print(f"  GPU: ₹{build.get('gpu_inr'):,}")
print(f"  Motherboard: ₹{build.get('motherboard_inr'):,}")
print(f"  RAM: ₹{build.get('ram_inr'):,}")
print(f"  Storage: ₹{build.get('storage_inr'):,}")
print(f"  PSU: ₹{build.get('psu_inr'):,}")
print(f"  Case: ₹{build.get('case_inr'):,}")
print(f"  Cooling: ₹{build.get('cooling_inr'):,}")
print(f"\nTOTAL: ₹{build.get('total_inr'):,}")
print(f"Target Performance: {build.get('target_fps')}")

# Example 4: Search for Steam game
print("\n" + "-"*70)
print("EXAMPLE 4: Search for STEAM GAME - Fortnite")
print("-"*70)

result = analyzer.extract_game_requirements('fortnite')
print(f"\nGame: {result.get('game_name')}")
print(f"Type: {result.get('game_type')}")
print(f"Platforms: {', '.join(result.get('platforms', []))}")
print(f"Source: {result.get('source')}")
print(f"Notes: {result.get('notes', 'N/A')}")

# Example 5: Search for unknown game (fallback)
print("\n" + "-"*70)
print("EXAMPLE 5: Search for UNKNOWN GAME (Uses Fallback)")
print("-"*70)

result = analyzer.extract_game_requirements('some random indie game xyz')
print(f"\nGame: {result.get('game_name')}")
print(f"Source: {result.get('source')} (fallback)")
print(f"Notes: {result.get('notes', 'N/A')}")
print(f"\nGeneric Specs Generated:")
min_specs = result.get('minimum', {})
print(f"  Minimum RAM: {min_specs.get('ram_gb')}GB")
print(f"  Recommended RAM: {result.get('recommended', {}).get('ram_gb')}GB")
print(f"  High-End RAM: {result.get('high_end', {}).get('ram_gb')}GB")

# Example 6: PC Validation
print("\n" + "-"*70)
print("EXAMPLE 6: Validate PC for a Game")
print("-"*70)

pc_specs = {
    'cpu_cores': 8,
    'gpu_vram': 4,
    'ram_gb': 16
}

result = analyzer.validate_pc_for_game('minecraft', pc_specs)
print(f"\nGame: {result.get('game_name')}")
print(f"Your PC Specs: {pc_specs}")
print(f"Can Run: {'YES ✓' if result.get('can_run') else 'NO ✗'}")
print(f"Performance Level: {result.get('performance_level', 'Unknown')}")

# Example 7: Multiple games quick search
print("\n" + "-"*70)
print("EXAMPLE 7: Quick Search Multiple Games")
print("-"*70)

games_to_search = ['Valorant', 'GTA V', 'Cyberpunk', 'PUBG', 'Doom']
print(f"\nSearching for {len(games_to_search)} games...")

for game in games_to_search:
    result = analyzer.extract_game_requirements(game)
    source = result.get('source')
    game_name = result.get('game_name')
    print(f"  ✓ {game:15} → {game_name:30} (source: {source})")

print("\n" + "="*70)
print("DEMO COMPLETE")
print("="*70)
print("\nKey Points:")
print("  1. Database has 506 games ready for instant search")
print("  2. Searches are fuzzy-matched (case-insensitive, partial names work)")
print("  3. Unknown games get automatic fallback specs")
print("  4. Build recommendations include INR pricing")
print("  5. System never fails - always returns valid results")
print("\n" + "="*70 + "\n")
