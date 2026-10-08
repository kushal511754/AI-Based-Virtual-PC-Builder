#!/usr/bin/env python3
"""Check database compatibility data."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from server.utils.db import get_db_connection, dict_from_row

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute('SELECT id, name, socket_type FROM cpu LIMIT 3')
print('CPUs:')
for row in cursor.fetchall():
    r = dict_from_row(row)
    print(f"  {r['id']}: {r['name']} - {r['socket_type']}")

cursor.execute('SELECT id, name, socket_type FROM motherboard LIMIT 3')
print('\nMotherboards:')
for row in cursor.fetchall():
    r = dict_from_row(row)
    print(f"  {r['id']}: {r['name']} - {r['socket_type']}")

conn.close()
