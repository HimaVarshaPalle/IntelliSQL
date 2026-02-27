import sqlite3

conn   = sqlite3.connect("sales.db")  
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id              INTEGER PRIMARY KEY,
        name            TEXT,
        city            TEXT,
        purchase_amount INTEGER
    )
""")

cursor.execute("SELECT COUNT(*) FROM customers")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO customers (name, city, purchase_amount) VALUES ('Neerja', 'Kadapa', 2500)")
    cursor.execute("INSERT INTO customers (name, city, purchase_amount) VALUES ('Nikhil', 'Tirupati', 5000)")
    cursor.execute("INSERT INTO customers (name, city, purchase_amount) VALUES ('Rehman', 'Hyderabad', 7568)")
    print("Records inserted successfully.")
else:
    print("Records already exist, skipping insert.")

print("\nAll customers:")
cursor.execute("SELECT * FROM customers")
for row in cursor.fetchall():
    print(row)

conn.commit()
conn.close()
print("\nDatabase ready!")
