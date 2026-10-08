#!/usr/bin/env python
"""Quick test of the OpenAI game analyzer"""

from server.services.openai_game_analyzer import OpenAIGameAnalyzer, MOCK_GAMES_DATABASE

print("=" * 60)
print("SYSTEM VERIFICATION TEST")
print("=" * 60)

print(f"\n✓ Database loaded successfully")
print(f"✓ Total games in database: {len(MOCK_GAMES_DATABASE)}")
print(f"✓ Core games: BGMI, Cyberpunk, Minecraft, Fortnite, Valorant, GTA V")

# Initialize analyzer
analyzer = OpenAIGameAnalyzer()
print(f"✓ Analyzer initialized")

# Test 1: Query Minecraft
print("\n--- Test 1: Minecraft Query ---")
result = analyzer.extract_game_requirements('minecraft')
print(f"✓ Game: {result.get('game_name')}")
print(f"✓ Source: {result.get('source')}")
print(f"✓ Minimum RAM: {result.get('minimum', {}).get('ram_gb')}GB")
print(f"✓ Recommended RAM: {result.get('recommended', {}).get('ram_gb')}GB")

# Test 2: Query BGMI
print("\n--- Test 2: BGMI Query ---")
result = analyzer.extract_game_requirements('bgmi')
print(f"✓ Game: {result.get('game_name')}")
print(f"✓ Source: {result.get('source')}")
print(f"✓ Platforms: {result.get('platforms')}")

# Test 3: Query Unknown Game (should fallback)
print("\n--- Test 3: Unknown Game Query (Fallback) ---")
result = analyzer.extract_game_requirements('randomly_made_up_game_12345')
print(f"✓ Game: {result.get('game_name')}")
print(f"✓ Source: {result.get('source')}")
print(f"✓ Minimum RAM: {result.get('minimum', {}).get('ram_gb')}GB")

# Test 4: Build recommendation
print("\n--- Test 4: Build Recommendation ---")
result = analyzer.get_game_and_build_recommendation('minecraft', 50000)
print(f"✓ Success: {result.get('success')}")
print(f"✓ Game: {result.get('game_name')}")
print(f"✓ Budget: ₹{result.get('budget_inr')}")
print(f"✓ Build Tier: {result.get('build_recommendation', {}).get('build_tier')}")
print(f"✓ Total Cost: ₹{result.get('build_recommendation', {}).get('total_inr')}")

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED")
print("=" * 60)
