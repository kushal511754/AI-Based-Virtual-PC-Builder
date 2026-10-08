#!/usr/bin/env python
"""Quick database audit script."""
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM cpu')
print(f'CPUs: {cursor.fetchone()[0]}')

cursor.execute('SELECT COUNT(*) FROM gpu')
print(f'GPUs: {cursor.fetchone()[0]}')

cursor.execute('SELECT COUNT(*) FROM motherboard')
print(f'Motherboards: {cursor.fetchone()[0]}')

cursor.execute('SELECT COUNT(*) FROM ram')
print(f'RAM: {cursor.fetchone()[0]}')

cursor.execute('SELECT COUNT(*) FROM storage')
print(f'Storage: {cursor.fetchone()[0]}')

cursor.execute('SELECT COUNT(*) FROM psu')
print(f'PSU: {cursor.fetchone()[0]}')

cursor.execute('SELECT COUNT(*) FROM pc_case')
print(f'Cases: {cursor.fetchone()[0]}')

cursor.execute('SELECT COUNT(*) FROM cooling')
print(f'Cooling: {cursor.fetchone()[0]}')

print('\n--- Sample CPUs ---')
cursor.execute('SELECT name, socket_type, cores, price FROM cpu LIMIT 3')
for row in cursor.fetchall():
    print(f'{row[0]}: {row[1]}, {row[2]} cores, Price: {row[3]}')

print('\n--- Sample GPUs ---')
cursor.execute('SELECT name, vram_gb, price FROM gpu LIMIT 3')
for row in cursor.fetchall():
    print(f'{row[0]}: {row[1]}GB, Price: {row[2]}')

print('\n--- Sample Motherboards ---')
cursor.execute('SELECT name, socket_type, price FROM motherboard LIMIT 3')
for row in cursor.fetchall():
    print(f'{row[0]}: {row[1]}, Price: {row[2]}')

conn.close()
