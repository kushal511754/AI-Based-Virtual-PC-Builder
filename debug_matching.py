#!/usr/bin/env python
"""Debug the search logic"""
import sys
sys.path.insert(0, '.')

from server.services.realtime_component_fetcher import RealtimeComponentFetcher

fetcher = RealtimeComponentFetcher()
db = fetcher._get_expanded_component_database()

print("Motherboards in database:")
for mb in db['motherboard']:
    print(f"  - {mb['name']}")

print("\nTesting matching for 'MSI B450 Tomahawk':")
result = fetcher._search_expanded_database('MSI B450 Tomahawk', 'motherboard')
print(f"Result: {result}")

if result:
    print(f"Found: {result['name']}")
else:
    print("No match found!")

# Let's manually check the scoring
import re
query = 'MSI B450 Tomahawk'
query_clean = re.sub(r'\s*\([^)]*\)\s*', ' ', query).strip()
query_lower = query_clean.lower()

print(f"\nManual scoring for query: '{query_lower}'")
for mb in db['motherboard']:
    name_lower = mb['name'].lower()
    score = 0
    
    # Strategy 1: Exact substring
    if query_lower in name_lower or name_lower in query_lower:
        score += 10
    
    # Strategy 2: Word matching
    query_words = query_lower.split()
    comp_words = name_lower.split()
    matches = 0
    for word in query_words:
        if len(word) >= 2 and word in name_lower:
            matches += 1
            score += 3
    
    print(f"  {mb['name']:30} score={score:3} (substring={query_lower in name_lower or name_lower in query_lower}, word_matches={matches})")
