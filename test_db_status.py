#!/usr/bin/env python
"""Test database status and component counts."""
from server.utils.db import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

# Check what tables exist and have data
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables:', [t[0] for t in tables])
print()

# Check if any components exist
component_tables = ['cpu', 'gpu', 'motherboard', 'ram', 'storage', 'psu', 'pc_case', 'cooling']
for table in component_tables:
    cursor.execute(f'SELECT COUNT(*) FROM {table}')
    count = cursor.fetchone()[0]
    print(f'{table}: {count} records')
    if count > 0:
        cursor.execute(f'SELECT id, name, price FROM {table} LIMIT 2')
        samples = cursor.fetchall()
        for row in samples:
            print(f'  - {row}')

conn.close()
