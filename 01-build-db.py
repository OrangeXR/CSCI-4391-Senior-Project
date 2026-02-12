import sqlite3

# Creates a database named inventory.db with 5 fields: id(Primary Key), name, category, quantity, best_by

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    best_by TEXT NOT NULL
)
""")
   
conn.commit()
conn.close()
