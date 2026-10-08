#!/usr/bin/env python
"""Test the matching logic"""
import re

query = "MSI B450 Tomahawk (AM4)"
query_clean = re.sub(r'\s*\([^)]*\)\s*', ' ', query).strip()
query_lower = query_clean.lower()

db_name = "MSI B450 Tomahawk"
db_name_lower = db_name.lower()

print(f"Original query: {query}")
print(f"Cleaned query: {query_clean}")
print(f"Lowercase query: {query_lower}")
print(f"DB name: {db_name}")
print(f"Lowercase DB: {db_name_lower}")
print()
print(f"Direct substring match: {query_lower in db_name_lower or db_name_lower in query_lower}")
print(f"query_lower == db_name_lower: {query_lower == db_name_lower}")
