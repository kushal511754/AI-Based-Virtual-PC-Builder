#!/usr/bin/env python
"""
QUICK START EXAMPLES - Copy-Paste Ready
Simple examples to get started immediately
"""

from server.services.openai_game_analyzer import OpenAIGameAnalyzer

# Initialize once
analyzer = OpenAIGameAnalyzer()

print("\n" + "="*70)
print("QUICK START EXAMPLES - Copy-Paste Ready")
print("="*70)

# ========================================================================
# EXAMPLE 1: Search a game
# ========================================================================
print("\n📌 EXAMPLE 1: Search for a game")
print("-" * 70)
print("Code:")
print("""
result = analyzer.extract_game_requirements('minecraft')
print(f"Game: {result['game_name']}")
print(f"Platforms: {result['platforms']}")
print(f"Recommended RAM: {result['recommended']['ram_gb']}GB")
""")
print("\nResult:")
result = analyzer.extract_game_requirements('minecraft')
print(f"Game: {result['game_name']}")
print(f"Platforms: {result['platforms']}")
print(f"Recommended RAM: {result['recommended']['ram_gb']}GB")

# ========================================================================
# EXAMPLE 2: Get build recommendation
# ========================================================================
print("\n" + "-" * 70)
print("📌 EXAMPLE 2: Get PC build for a game and budget")
print("-" * 70)
print("Code:")
print("""
result = analyzer.get_game_and_build_recommendation('Fortnite', 75000)
build = result['build_recommendation']
print(f"Game: {result['game_name']}")
print(f"Build Tier: {build['build_tier']}")
print(f"Total Cost: ₹{build['total_inr']:,}")
print(f"Performance: {build['target_fps']}")
""")
print("\nResult:")
result = analyzer.get_game_and_build_recommendation('Fortnite', 75000)
build = result['build_recommendation']
print(f"Game: {result['game_name']}")
print(f"Build Tier: {build['build_tier']}")
print(f"Total Cost: ₹{build['total_inr']:,}")
print(f"Performance: {build['target_fps']}")

# ========================================================================
# EXAMPLE 3: Check components for specific budget
# ========================================================================
print("\n" + "-" * 70)
print("📌 EXAMPLE 3: See component breakdown for budget")
print("-" * 70)
print("Code:")
print("""
result = analyzer.get_game_and_build_recommendation('BGMI', 50000)
build = result['build_recommendation']
print(f"Budget: ₹{result['budget']:,}")
print(f"CPU: ₹{build['cpu_inr']:,}")
print(f"GPU: ₹{build['gpu_inr']:,}")
print(f"RAM: ₹{build['ram_inr']:,}")
print(f"Total: ₹{build['total_inr']:,}")
""")
print("\nResult:")
result = analyzer.get_game_and_build_recommendation('BGMI', 50000)
build = result['build_recommendation']
print(f"Budget: ₹{result['budget_inr']:,}")
print(f"CPU: ₹{build['cpu_inr']:,}")
print(f"GPU: ₹{build['gpu_inr']:,}")
print(f"RAM: ₹{build['ram_inr']:,}")
print(f"Total: ₹{build['total_inr']:,}")

# ========================================================================
# EXAMPLE 4: Validate PC specs
# ========================================================================
print("\n" + "-" * 70)
print("📌 EXAMPLE 4: Check if your PC can run a game")
print("-" * 70)
print("Code:")
print("""
pc = {'cpu_cores': 8, 'gpu_vram': 4, 'ram_gb': 16}
result = analyzer.validate_pc_for_game('Cyberpunk 2077', pc)
print(f"Can run: {'YES ✓' if result['can_run'] else 'NO ✗'}")
""")
print("\nResult:")
pc = {'cpu_cores': 8, 'gpu_vram': 4, 'ram_gb': 16}
result = analyzer.validate_pc_for_game('Cyberpunk 2077', pc)
print(f"Can run: {'YES ✓' if result['can_run'] else 'NO ✗'}")

# ========================================================================
# EXAMPLE 5: Get all spec levels for a game
# ========================================================================
print("\n" + "-" * 70)
print("📌 EXAMPLE 5: See minimum, recommended, and high-end specs")
print("-" * 70)
print("Code:")
print("""
result = analyzer.extract_game_requirements('Cyberpunk 2077')
print(f"Minimum RAM: {result['minimum']['ram_gb']}GB")
print(f"Recommended RAM: {result['recommended']['ram_gb']}GB")
print(f"High-End RAM: {result['high_end']['ram_gb']}GB")
""")
print("\nResult:")
result = analyzer.extract_game_requirements('Cyberpunk 2077')
print(f"Minimum RAM: {result['minimum']['ram_gb']}GB")
print(f"Recommended RAM: {result['recommended']['ram_gb']}GB")
print(f"High-End RAM: {result['high_end']['ram_gb']}GB")

# ========================================================================
# EXAMPLE 6: Search multiple games
# ========================================================================
print("\n" + "-" * 70)
print("📌 EXAMPLE 6: Search multiple games quickly")
print("-" * 70)
print("Code:")
print("""
games = ['Valorant', 'Portal', 'Doom', 'Unknown Game']
for game in games:
    result = analyzer.extract_game_requirements(game)
    source = result['source']
    print(f"{game}: {source}")
""")
print("\nResult:")
games = ['Valorant', 'Portal', 'Doom', 'Unknown Game']
for game in games:
    result = analyzer.extract_game_requirements(game)
    source = result['source']
    print(f"{game}: {source}")

# ========================================================================
# EXAMPLE 7: Different budgets
# ========================================================================
print("\n" + "-" * 70)
print("📌 EXAMPLE 7: Get builds for different budgets")
print("-" * 70)
print("Code:")
print("""
budgets = [50000, 100000, 150000]
for budget in budgets:
    result = analyzer.get_game_and_build_recommendation('GTA V', budget)
    build = result['build_recommendation']
    print(f"₹{budget:,}: {build['build_tier']} (Total: ₹{build['total_inr']:,})")
""")
print("\nResult:")
budgets = [50000, 100000, 150000]
for budget in budgets:
    result = analyzer.get_game_and_build_recommendation('GTA V', budget)
    build = result['build_recommendation']
    print(f"₹{budget:,}: {build['build_tier']} (Total: ₹{build['total_inr']:,})")

# ========================================================================
# EXAMPLE 8: Get performance targets
# ========================================================================
print("\n" + "-" * 70)
print("📌 EXAMPLE 8: See estimated FPS")
print("-" * 70)
print("Code:")
print("""
result = analyzer.extract_game_requirements('Minecraft')
fps = result['estimated_fps']
for resolution, fps_range in fps.items():
    print(f"{resolution}: {fps_range}")
""")
print("\nResult:")
result = analyzer.extract_game_requirements('Minecraft')
fps = result['estimated_fps']
for resolution, fps_range in fps.items():
    print(f"{resolution}: {fps_range}")

# ========================================================================
# QUICK REFERENCE
# ========================================================================
print("\n" + "="*70)
print("QUICK REFERENCE")
print("="*70)

print("""
Available Games in Database (506 total):

CORE GAMES (6):
  • BGMI
  • Cyberpunk 2077
  • Minecraft
  • Fortnite
  • Valorant
  • GTA V

STEAM GAMES (500):
  • Doom, Portal, Half-Life, CS:GO, Dota 2, and more...

UNKNOWN GAMES:
  • Any game name works - returns automatic fallback specs!

Budget Tiers:
  • ₹20K-40K   → Budget   (1080p 60fps)
  • ₹40K-80K   → Mid-Range (1440p 60fps)
  • ₹80K-150K  → High-End (1440p 100fps)
  • ₹150K+     → Enthusiast (4K 60fps)

Main Methods:
  • analyzer.extract_game_requirements(game_name)
  • analyzer.get_game_and_build_recommendation(game_name, budget)
  • analyzer.validate_pc_for_game(game_name, pc_specs)

Return Values are JSON/Dicts with:
  • game_name: Game title
  • game_type: Genre
  • platforms: List of platforms
  • source: 'database', 'openai', or 'fallback'
  • minimum/recommended/high_end: Spec levels
  • estimated_fps: FPS at different resolutions
  • build_recommendation: Component costs in INR
""")

print("="*70 + "\n")
