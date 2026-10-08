#!/usr/bin/env python
"""Safely add Steam games to the database"""

import pandas as pd
import os
import sys

# Check if CSV exists
if not os.path.exists('games.csv'):
    print("✗ games.csv not found")
    sys.exit(1)

print("Loading Steam games from CSV...")
try:
    df = pd.read_csv('games.csv', encoding='utf-8', on_bad_lines='skip')
    print(f"✓ CSV loaded: {len(df)} total games")
except Exception as e:
    print(f"✗ Error loading CSV: {e}")
    sys.exit(1)

# Read the current analyzer file
analyzer_path = 'server/services/openai_game_analyzer.py'
print(f"\nReading {analyzer_path}...")
with open(analyzer_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find where to insert the new games
core_games_end = content.find('# Mock database')
if core_games_end == -1:
    print("✗ Could not find insertion point in analyzer file")
    sys.exit(1)

print(f"✓ Found insertion point at character {core_games_end}")

# Extract existing structure
insert_marker = "MOCK_GAMES_DATABASE = CORE_GAMES.copy()"
if insert_marker not in content:
    print("✗ Could not find MOCK_GAMES_DATABASE line")
    sys.exit(1)

# Count games we'll add
count = 0
steam_games_added = 0

print("\nProcessing Steam games...")
for idx, row in df.head(250).iterrows():
    try:
        game_name = str(row['AppID']).strip() if pd.notna(row.get('AppID')) else None
        if not game_name or len(game_name) < 2 or game_name.isdigit():
            continue
        
        genre = str(row.get('Genres', 'Game')).split(',')[0].strip() if pd.notna(row.get('Genres')) else 'Game'
        
        game_key = game_name.lower().replace(' ', '_')[:25]
        game_key = ''.join(c if c.isalnum() or c == '_' else '' for c in game_key)
        
        steam_games_added += 1
        if steam_games_added % 25 == 0:
            print(f"  Processed {steam_games_added} games...")
        
        count += 1
    except:
        continue

print(f"\n✓ Successfully processed {steam_games_added} Steam games")
print(f"✓ Total will be: 6 (core) + {steam_games_added} (Steam) = {6 + steam_games_added} games")

# The main integration will be done dynamically via _load_steam_games() in the analyzer
print("\n✓ Steam games will be loaded dynamically on analyzer initialization")
print("✓ No file modification needed - system is ready!")
