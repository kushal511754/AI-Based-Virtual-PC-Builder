#!/usr/bin/env python
"""
Parse Steam Games CSV datasets and integrate into game analyzer.
Supports: Martin Bustos games.csv + archive.zip files
Extracts game names, genres, and infers specs from descriptions.
"""

import pandas as pd
import json
import re
from pathlib import Path

# Game specs patterns to extract from descriptions
CPU_PATTERNS = [
    r'(?:i3|i5|i7|i9|Ryzen 3|Ryzen 5|Ryzen 7|Ryzen 9)',
    r'(?:quad.?core|dual.?core|multi.?core|multi.?threaded)',
    r'(?:2\.0\s*GHz|2\.5\s*GHz|3\.0\s*GHz|3\.5\s*GHz)',
]

GPU_PATTERNS = [
    r'(?:GTX|RTX|Radeon|GeForce|Arc)',
    r'(?:1050|1060|1070|1080|2060|2070|3060|3070|4060|4070)',
    r'(?:GB\s+VRAM|GB\s+memory)',
]

RAM_PATTERNS = [
    r'(?:(\d+)\s*(?:GB|gb|Gb)\s+(?:RAM|memory|of RAM))',
    r'(?:at least|minimum|requires)\s+(\d+)\s*(?:GB|gb)',
]

def extract_specs_from_description(description):
    """Extract hardware specs from game description/requirements."""
    if not isinstance(description, str):
        return None
    
    specs = {}
    
    # Look for CPU cores
    if 'quad' in description.lower() or '4 core' in description.lower():
        specs['cpu_cores'] = 4
    elif 'dual' in description.lower() or '2 core' in description.lower():
        specs['cpu_cores'] = 2
    elif '8 core' in description.lower() or 'octa' in description.lower():
        specs['cpu_cores'] = 8
    
    # Look for GPU VRAM
    vram_match = re.search(r'(\d+)\s*(?:GB|gb)\s+(?:VRAM|GPU|dedicated)', description)
    if vram_match:
        specs['gpu_vram'] = int(vram_match.group(1))
    
    # Look for RAM
    ram_match = re.search(r'(\d+)\s*(?:GB|gb)\s+(?:RAM|memory)', description)
    if ram_match:
        specs['ram_gb'] = int(ram_match.group(1))
    
    return specs if specs else None

def parse_games_csv(csv_path, max_games=5000):
    """Parse Martin Bustos games.csv file."""
    print(f"Reading {csv_path}...")
    
    try:
        # Read CSV with different encoding attempts
        try:
            df = pd.read_csv(csv_path, encoding='utf-8', on_bad_lines='skip')
        except:
            df = pd.read_csv(csv_path, encoding='latin-1', on_bad_lines='skip')
        
        print(f"✓ CSV loaded: {len(df)} rows")
        
        games = []
        for idx, row in df.head(max_games).iterrows():
            try:
                # IMPORTANT: Game name is in 'AppID' column, not 'Name'!
                game_name = None
                if 'AppID' in df.columns and pd.notna(row['AppID']):
                    game_name = str(row['AppID']).strip()
                
                if not game_name or len(game_name) < 2 or game_name.isdigit():
                    continue
                
                # Get description
                description = ""
                if 'About the game' in df.columns and pd.notna(row['About the game']):
                    description = str(row['About the game'])
                
                # Get genres
                genre = "Game"
                if 'Genres' in df.columns and pd.notna(row['Genres']):
                    genres = str(row['Genres']).split(',')
                    genre = genres[0].strip() if genres else 'Game'
                
                # Get platforms
                platforms = ['PC']
                if 'Windows' in df.columns:
                    try:
                        if pd.notna(row['Windows']) and str(row['Windows']).lower() == 'true':
                            platforms = ['Windows']
                    except:
                        pass
                
                # Try to extract specs from description
                specs = extract_specs_from_description(description)
                
                game_data = {
                    'game_name': game_name,
                    'platforms': platforms,
                    'game_type': str(genre) if genre else 'Game',
                    'release_year': 2024,
                    'minimum': {
                        'cpu_cores': specs.get('cpu_cores', 4) if specs else 4,
                        'cpu_name': 'Intel i5 / AMD Ryzen 5',
                        'gpu_vram': specs.get('gpu_vram', 2) if specs else 2,
                        'gpu_name': 'GTX 1050 / RX 560',
                        'ram_gb': specs.get('ram_gb', 8) if specs else 8,
                        'storage_gb': 50,
                        'os': 'Windows 10/11 64-bit'
                    },
                    'recommended': {
                        'cpu_cores': max(8, (specs.get('cpu_cores', 4) + 4) if specs else 8),
                        'cpu_name': 'Intel i7 / AMD Ryzen 7',
                        'gpu_vram': max(4, (specs.get('gpu_vram', 2) * 2) if specs else 4),
                        'gpu_name': 'RTX 2070 / RX 5700 XT',
                        'ram_gb': max(16, (specs.get('ram_gb', 8) * 2) if specs else 16),
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
                    'notes': f'Steam game - {genre}',
                    'source': 'steam_dataset'
                }
                
                games.append(game_data)
                
                if (idx + 1) % 500 == 0:
                    print(f"  Processed {idx + 1} games...")
            
            except Exception as e:
                continue
        
        print(f"✓ Extracted {len(games)} valid games from CSV")
        return games
    
    except Exception as e:
        print(f"✗ Error reading CSV: {e}")
        return []

def update_game_analyzer(games):
    """Update openai_game_analyzer.py with new games."""
    
    analyzer_path = Path('server/services/openai_game_analyzer.py')
    
    # Read current file
    with open(analyzer_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create new database dict with proper game name keys
    db_lines = []
    for game in games:
        # Use game name as key (lowercase, clean)
        game_key = game['game_name'].lower().replace(' ', '_').replace(':', '').replace('"', '')[:30]
        game_key = ''.join(c if c.isalnum() or c == '_' else '' for c in game_key)  # Remove special chars
        
        # Format game data as JSON
        game_json = json.dumps(game, indent=12, ensure_ascii=False)
        db_lines.append(f"    '{game_key}': {game_json},")
    
    db_dict = "{\n" + "\n".join(db_lines) + "\n}"
    
    # Find and replace MOCK_GAMES_DATABASE
    old_db_start = content.find("MOCK_GAMES_DATABASE = {")
    old_db_end = content.find("\n}\n\n", old_db_start) + 3
    
    if old_db_start != -1 and old_db_end != -1:
        new_content = (
            content[:old_db_start] +
            "MOCK_GAMES_DATABASE = " +
            db_dict +
            content[old_db_end:]
        )
        
        with open(analyzer_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Updated openai_game_analyzer.py with {len(games)} games")
        return True
    else:
        print("✗ Could not find MOCK_GAMES_DATABASE in openai_game_analyzer.py")
        return False

if __name__ == '__main__':
    print("=" * 70)
    print("STEAM GAMES DATASET INTEGRATION")
    print("=" * 70)
    
    # Parse games.csv
    csv_path = Path('games.csv')
    if csv_path.exists():
        print(f"\n1. Parsing {csv_path.name}...")
        games = parse_games_csv(str(csv_path), max_games=2000)
        
        if games:
            print(f"\n2. Updating game analyzer...")
            if update_game_analyzer(games):
                print("\n✓ SUCCESS! Dataset integrated")
                print(f"✓ Added {len(games)} games to database")
                print("\nNext step: Restart the server and test!")
            else:
                print("✗ Failed to update analyzer")
        else:
            print("✗ No games extracted")
    else:
        print(f"✗ {csv_path.name} not found in current directory")
    
    print("=" * 70)
