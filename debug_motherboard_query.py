#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('/Users/LEENOVO/Desktop/projectk/database.db')
cursor = conn.cursor()

print("=== ALL MOTHERBOARDS IN DATABASE ===")
cursor.execute("SELECT id, name, socket_type, price FROM motherboard")
motherboards = cursor.fetchall()
for mb in motherboards:
    print(f"ID: {mb[0]}, Name: {mb[1]}, Socket: {mb[2]}, Price: {mb[3]}")

print("\n=== ALL CPUs IN DATABASE ===")
cursor.execute("SELECT id, name, socket_type, price FROM cpu")
cpus = cursor.fetchall()
for cpu in cpus:
    print(f"ID: {cpu[0]}, Name: {cpu[1]}, Socket: {cpu[2]}, Price: {cpu[3]}")

print("\n=== TEST QUERY ===")
# Test the exact query that would be used for gaming domain with $2000 budget
# Gaming domain allocates: cpu: 20% = $400, motherboard: 10% = $200
socket_type = 'LGA1700'  # Most likely socket from CPU
motherboard_budget = 200

print(f"Query: socket_type={socket_type}, price <= {motherboard_budget}")
cursor.execute(
    "SELECT id, name, socket_type, price FROM motherboard WHERE socket_type = ? AND price <= ? ORDER BY price DESC LIMIT 1",
    (socket_type, motherboard_budget)
)
result = cursor.fetchone()
print(f"Result: {result}")

if not result:
    print("\nNo motherboard found! Let's try without budget limit:")
    cursor.execute(
        "SELECT id, name, socket_type, price FROM motherboard WHERE socket_type = ? ORDER BY price DESC LIMIT 1",
        (socket_type,)
    )
    result = cursor.fetchone()
    print(f"Result: {result}")

conn.close()
