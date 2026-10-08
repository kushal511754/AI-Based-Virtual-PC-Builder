#!/usr/bin/env python
"""
Integrate Steam Games from CSV/JSON into the game analyzer database.
Extracts top 500 popular games and adds them to MOCK_GAMES_DATABASE.
"""

import pandas as pd
import json
import re
from pathlib import Path

def extract_specs_from_description(description):
    """Extract hardware specs from game description."""
    if not isinstance(description, str) or len(description) < 10:
        return {}
    
    specs = {}
    desc_lower = description.lower()
    
    # CPU cores
    if any(x in desc_lower for x in ['quad core', '4 core', 'quad-core']):
        specs['cpu_cores'] = 4
    elif any(x in desc_lower for x in ['octa core', '8 core', 'octa-core']):
        specs['cpu_cores'] = 8
    
    # GPU VRAM
    vram_match = re.search(r'(\d+)\s*(?:gb|gb vram)', desc_lower)
    if vram_match:
        specs['gpu_vram'] = int(vram_match.group(1))
    
    # RAM
    ram_match = re.search(r'(\d+)\s*(?:gb|gb ram)', desc_lower)
    if ram_match:
        specs['ram_gb'] = int(ram_match.group(1))
    
    return specs

def parse_steam_csv(csv_path, limit=500):
    """Parse Martin Bustos Steam games.csv"""
    print(f"Parsing {csv_path}...")
    
    try:
        df = pd.read_csv(csv_path, encoding='utf-8', on_bad_lines='skip')
        print(f"✓ Loaded {len(df)} games from CSV")
        
        games = []
        for idx, row in df.head(limit).iterrows():
            try:
                # Game name is in 'AppID' column
                game_name = str(row['AppID']).strip() if pd.notna(row.get('AppID')) else None
                
                if not game_name or len(game_name) < 2 or game_name.isdigit():
                    continue
                
                # Get description
                description = str(row.get('About the game', '')) if pd.notna(row.get('About the game')) else ''
                
                # Get genres
                genres = str(row.get('Genres', 'Game')).split(',')
                genre = genres[0].strip() if genres else 'Game'
                
                # Extract specs from description
                specs = extract_specs_from_description(description)
                
                game_data = {
                    'game_name': game_name,
                    'platforms': ['PC'],
                    'game_type': genre,
                    'release_year': 2024,
                    'minimum': {
                        'cpu_cores': specs.get('cpu_cores', 4),
                        'cpu_name': 'Intel i5 / AMD Ryzen 5',
                        'gpu_vram': specs.get('gpu_vram', 2),
                        'gpu_name': 'GTX 1050 / RX 560',
                        'ram_gb': specs.get('ram_gb', 8),
                        'storage_gb': 50,
                        'os': 'Windows 10/11 64-bit'
                    },
                    'recommended': {
                        'cpu_cores': max(8, specs.get('cpu_cores', 4) + 2),
                        'cpu_name': 'Intel i7 / AMD Ryzen 7',
                        'gpu_vram': max(4, specs.get('gpu_vram', 2) * 2),
                        'gpu_name': 'RTX 2070 / RX 5700 XT',
                        'ram_gb': max(16, specs.get('ram_gb', 8) * 2),
                        'storage_gb': 100,
                        'os': 'Windows 11 64-bit'
                    },
                    'high_end': {
                        'cpu_cores': 12,
                        'cpu_name': 'Intel i9 / AMD Ryzen 9',
                        'gpu_vram': 8,
                        'gpu_name': 'RTX 4070 / RX 7900 XT',
                        'ram_gb': 32,
                        'storage_gb': 150,
                        'os': 'Windows 11 64-bit'
                    },
                    'estimated_fps': {
                        '1080p_high': '60-90 FPS',
                        '1440p_high': '40-60 FPS',
                        '4k_high': '20-30 FPS'
                    },
                    'special_requirements': [],
                    'notes': f'Steam - {genre}',
                    'source': 'steam_dataset'
                }
                
                games.append(game_data)
                
                if (idx + 1) % 100 == 0:
                    print(f"  Processed {idx + 1} games...")
                    
            except Exception as e:
                continue
        
        print(f"✓ Extracted {len(games)} games")
        return games
    
    except Exception as e:
        print(f"✗ Error reading CSV: {e}")
        return []

def add_games_to_analyzer(games):
    """Add games to openai_game_analyzer.py MOCK_GAMES_DATABASE"""
    
    analyzer_path = Path('server/services/openai_game_analyzer.py')
    
    if not analyzer_path.exists():
        print("✗ openai_game_analyzer.py not found")
        return False
    
    # Read file
    with open(analyzer_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the line with "}" that closes MOCK_GAMES_DATABASE
    db_end = -1
    for i, line in enumerate(lines):
        if "}\n" in line and i > 100:  # Skip early lines
            db_end = i
            break
    
    if db_end == -1:
        print("✗ Could not find database end")
        return False
    
    # Generate new game entries
    new_entries = []
    for game in games:
        game_key = game['game_name'].lower().replace(' ', '_')[:25]
        game_key = ''.join(c if c.isalnum() or c == '_' else '' for c in game_key)
        
        entry = f"    '{game_key}': {json.dumps(game, ensure_ascii=False)},\n"
        new_entries.append(entry)
    
    # Insert before the closing "}"
    new_lines = lines[:db_end] + new_entries + lines[db_end:]
    
    # Write back
    with open(analyzer_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✓ Added {len(games)} games to database")
    return True

if __name__ == '__main__':
    print("=" * 70)
    print("IMPLEMENTING STEAM DATASET")
    print("=" * 70)
    
    csv_path = Path('games.csv')
    if csv_path.exists():
        print(f"\n1. Parsing Steam CSV dataset...")
        games = parse_steam_csv(str(csv_path), limit=500)
        
        if games:
            print(f"\n2. Adding to analyzer database...")
            if add_games_to_analyzer(games):
                print(f"\n✓ SUCCESS! Dataset implemented")
                print(f"✓ Total games now: {len(games) + 6} (6 hardcoded + {len(games)} from Steam)")
                print(f"✓ Restart server to use new database!")
            else:
                print("✗ Failed to add games")
        else:
            print("✗ No games extracted")
    else:
        print(f"✗ {csv_path} not found")
    
    print("=" * 70)
