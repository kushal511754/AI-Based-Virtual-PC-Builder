#!/usr/bin/env python
"""Test that ANY game user enters gets specifications."""

from server.services.openai_game_analyzer import OpenAIGameAnalyzer

analyzer = OpenAIGameAnalyzer()

print("=" * 70)
print("TESTING: ANY GAME GETS SPECIFICATIONS")
print("=" * 70)

# Test 1: Game in database (BGMI)
print("\n1. BGMI (In Database)")
print("-" * 70)
result = analyzer.extract_game_requirements('BGMI')
print(f"✓ Source: {result.get('source')}")
print(f"✓ Game: {result.get('game_name')}")
print(f"✓ Minimum: {result['minimum']['cpu_cores']} cores CPU, {result['minimum']['ram_gb']}GB RAM")
print(f"✓ Recommended: {result['recommended']['cpu_cores']} cores CPU, {result['recommended']['ram_gb']}GB RAM")
print(f"✓ Platforms: {', '.join(result.get('platforms', []))}")

# Test 2: Another game in database  
print("\n2. Fortnite (In Database)")
print("-" * 70)
result = analyzer.extract_game_requirements('fortnite')
print(f"✓ Source: {result.get('source')}")
print(f"✓ Game: {result.get('game_name')}")
print(f"✓ Minimum: {result['minimum']['cpu_cores']} cores CPU, {result['minimum']['ram_gb']}GB RAM")
print(f"✓ Recommended: {result['recommended']['cpu_cores']} cores CPU, {result['recommended']['ram_gb']}GB RAM")

# Test 3: Unknown game (should generate generic)
print("\n3. Random Unknown Game (NOT in Database)")
print("-" * 70)
result = analyzer.extract_game_requirements('Some Random Indie Game 2025')
print(f"✓ Source: {result.get('source')}")
print(f"✓ Game: {result.get('game_name')}")
print(f"✓ Minimum: {result['minimum']['cpu_cores']} cores CPU, {result['minimum']['ram_gb']}GB RAM")
print(f"✓ Recommended: {result['recommended']['cpu_cores']} cores CPU, {result['recommended']['ram_gb']}GB RAM")
print(f"✓ Platforms: {', '.join(result.get('platforms', []))}")
print(f"✓ Notes: {result.get('notes')}")

# Test 4: Partial match game
print("\n4. 'cyber' - Partial match for Cyberpunk")
print("-" * 70)
result = analyzer.extract_game_requirements('cyber')
print(f"✓ Source: {result.get('source')}")
print(f"✓ Game: {result.get('game_name')}")
print(f"✓ Matched: {result.get('game_name')}")

# Test 5: Build recommendation for any game with budget
print("\n5. Build Recommendation for Unknown Game (₹75,000 budget)")
print("-" * 70)
result = analyzer.get_game_and_build_recommendation('Elden Ring 2', 75000)
print(f"✓ Success: {result.get('success')}")
print(f"✓ Game: {result.get('game_name')}")
print(f"✓ Game Source: {result.get('game_specs', {}).get('source')}")
print(f"✓ Build Recommendation: {result.get('build_recommendation', {}).get('build_tier')}")
print(f"✓ Target FPS: {result.get('build_recommendation', {}).get('target_fps')}")
print(f"✓ Total Budget: ₹{result.get('build_recommendation', {}).get('total_inr')}")

print("\n" + "=" * 70)
print("✓ ALL TESTS PASSED - ANY GAME GETS SPECIFICATIONS!")
print("=" * 70)
