#!/usr/bin/env python3
"""Test GTA V search and budget scaling."""

from server.services.openai_game_analyzer import OpenAIGameAnalyzer

a = OpenAIGameAnalyzer()

# Test GTA V search
print("=" * 60)
print("GTA V SEARCH TEST")
print("=" * 60)
gta_results = a.search_games('GTA')
print(f'Found {len(gta_results)} results for "GTA":')
for g in gta_results:
    print(f'  ✓ {g["name"]} ({g["source"]})')

# Test different budget builds for different games
print("\n" + "=" * 60)
print("BGMI - BUDGET SCALING TEST")
print("=" * 60)
for budget in [50000, 75000, 100000, 150000]:
    result = a.get_game_and_build_recommendation('BGMI', budget)
    build = result['build_recommendation']
    print(f'Budget ₹{budget:,}:')
    print(f'  - Total: ₹{build["total_inr"]:,}')
    print(f'  - GPU: ₹{build["gpu_inr"]:,}, CPU: ₹{build["cpu_inr"]:,}, RAM: ₹{build["ram_inr"]:,}')
    print(f'  - Tier: {build["build_tier"]} | Target: {build["target_fps"]}')

print("\n" + "=" * 60)
print("GTA V - BUDGET SCALING TEST")
print("=" * 60)
for budget in [50000, 100000, 150000]:
    result = a.get_game_and_build_recommendation('GTA V', budget)
    build = result['build_recommendation']
    print(f'Budget ₹{budget:,}:')
    print(f'  - Total: ₹{build["total_inr"]:,}')
    print(f'  - GPU: ₹{build["gpu_inr"]:,}, CPU: ₹{build["cpu_inr"]:,}, RAM: ₹{build["ram_inr"]:,}')
    print(f'  - Tier: {build["build_tier"]} | Target: {build["target_fps"]}')

print("\n" + "=" * 60)
print("MINECRAFT - BUDGET SCALING TEST")
print("=" * 60)
for budget in [40000, 75000, 120000]:
    result = a.get_game_and_build_recommendation('Minecraft', budget)
    build = result['build_recommendation']
    print(f'Budget ₹{budget:,}:')
    print(f'  - Total: ₹{build["total_inr"]:,}')
    print(f'  - GPU: ₹{build["gpu_inr"]:,}, CPU: ₹{build["cpu_inr"]:,}, RAM: ₹{build["ram_inr"]:,}')
    print(f'  - Tier: {build["build_tier"]} | Target: {build["target_fps"]}')

print("\n✅ All tests completed!")
