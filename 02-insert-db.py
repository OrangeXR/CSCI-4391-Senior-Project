import sqlite3

sample_items = [
    ("Black Beans", "Canned", 2, "2026-03-01"),
    ("Milk", "Dairy", 1, "2026-02-12"),
    ("Apples", "Produce", 5, "2026-02-15"),
    ("Bread", "Bakery", 1, "2026-02-11"),
    ("Yogurt", "Dairy", 3, "2026-02-13"),
    ("Tomatoes", "Produce", 4, "2026-02-14")
]

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

cursor.executemany("""
INSERT INTO inventory (name, category, quantity, best_by)
Values (?,?,?,?)
""", sample_items)

conn.commit()
conn.close()
