import sqlite3

# Step 1: Connect to database (creates sales.db if it doesn't exist)
conn   = sqlite3.connect("sales.db")   # ← was "sales,db" — comma was the bug!
cursor = conn.cursor()

# Step 2: Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id              INTEGER PRIMARY KEY,
        name            TEXT,
        city            TEXT,
        purchase_amount INTEGER
    )
""")

# Step 3: Insert records (only if table is empty)
cursor.execute("SELECT COUNT(*) FROM customers")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO customers (name, city, purchase_amount) VALUES ('Neerja', 'Kadapa', 2500)")
    cursor.execute("INSERT INTO customers (name, city, purchase_amount) VALUES ('Nikhil', 'Tirupati', 5000)")
    cursor.execute("INSERT INTO customers (name, city, purchase_amount) VALUES ('Rehman', 'Hyderabad', 7568)")
    print("Records inserted successfully.")
else:
    print("Records already exist, skipping insert.")

# Step 4: Verify data
print("\nAll customers:")
cursor.execute("SELECT * FROM customers")
for row in cursor.fetchall():
    print(row)

# Step 5: Commit and close
conn.commit()
conn.close()
print("\nDatabase ready!")