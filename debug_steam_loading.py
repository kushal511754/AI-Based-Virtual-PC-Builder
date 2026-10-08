#!/usr/bin/env python
"""Detailed Steam games loading test"""

# Import the module first
import server.services.openai_game_analyzer as analyzer_module

print(f"BEFORE analyzer init: {len(analyzer_module.MOCK_GAMES_DATABASE)} games")

# Now create analyzer (which loads Steam games)
analyzer = analyzer_module.OpenAIGameAnalyzer()

# Check AFTER
print(f"AFTER analyzer init: {len(analyzer_module.MOCK_GAMES_DATABASE)} games")

# Check for steam games
steam_count = sum(1 for g in analyzer_module.MOCK_GAMES_DATABASE.values() if 'steam' in g.get('notes', '').lower())
print(f"\nGames with 'steam' in notes: {steam_count}")

# List keys
keys = list(analyzer_module.MOCK_GAMES_DATABASE.keys())
print(f"\nTotal unique game keys: {len(keys)}")
print(f"First 10 game keys: {keys[:10]}")

if len(keys) > 10:
    print(f"Last 10 game keys: {keys[-10:]}")
    
    # List a few examples
    print(f"\nExample games from position 6-10:")
    for key in keys[6:10]:
        game = analyzer_module.MOCK_GAMES_DATABASE[key]
        print(f"  {key}: {game.get('game_name')} ({game.get('source')})")
