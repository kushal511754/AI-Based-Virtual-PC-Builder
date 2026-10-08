#!/usr/bin/env python
"""Test the search endpoint"""
import logging
logging.basicConfig(level=logging.DEBUG)

from server.services.realtime_component_fetcher import RealtimeComponentFetcher

print("Creating fetcher...")
fetcher = RealtimeComponentFetcher()

print("Getting database...")
db = fetcher._get_expanded_component_database()
print(f"Database has {len(db)} component types")

print("\nSearching for MSI B450 Tomahawk (AM4)...")
result = fetcher.search_component("MSI B450 Tomahawk (AM4)", "motherboard")
print(f"Result success: {result.get('success')}")
if result.get("success"):
    comp = result["component"]
    print(f"Component: {comp['name']}")
    print(f"Price INR: {comp['price_inr']}")
    print(f"Price USD: {comp['price_usd']}")
    print(f"Socket: {comp.get('socket')}")
    print(f"Retailers: {len(comp.get('retailers', []))}")
else:
    print(f"Error: {result.get('error')}")
