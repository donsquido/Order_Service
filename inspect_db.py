import sqlite3
conn = sqlite3.connect("instance/orders.db")   
cur = conn.cursor()

print("Tables:")
for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    print(row[0])

print("\nSchema customer:")
row = cur.execute("SELECT sql FROM sqlite_master WHERE name='customer'").fetchone()
print(row[0] if row else "Table not found")

print("\nSchema order:")
print(cur.execute("SELECT sql FROM sqlite_master WHERE name='order'").fetchone()[0])

print("\nSchema order_item:")
print(cur.execute("SELECT sql FROM sqlite_master WHERE name='order_item'").fetchone()[0])

print("\nCustomer rows:")
for row in cur.execute("SELECT * FROM customer LIMIT 5"):
    print(row)

print("\nOrder rows:")
for row in cur.execute('SELECT * FROM "order" LIMIT 5'):
    print(row)

conn.close()
