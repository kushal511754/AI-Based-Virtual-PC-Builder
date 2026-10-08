#!/usr/bin/env python
from server.services.realtime_component_fetcher import RealtimeComponentFetcher
import re

query = 'MSI B450 Tomahawk (AM4)'
print(f'Original query: {query}')

# Test the regex
query_clean = re.sub(r'\s*\([^)]*\)\s*', ' ', query).strip()
print(f'Cleaned query: {query_clean}')

# Now test fetcher
fetcher = RealtimeComponentFetcher()
result = fetcher.search_component(query, 'motherboard')
print(f'Success: {result.get("success")}')
if result.get('success'):
    comp = result['component']
    print(f'Component: {comp["name"]}')
    print(f'Price INR: {comp["price_inr"]}')
    print(f'Socket: {comp.get("socket")}')
    print(f'Retailers: {len(comp.get("retailers", []))}')
else:
    print(f'Error: {result.get("error")}')
