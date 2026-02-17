import sqlite3

# Inserts sample players and items into inventory.db

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# ===============
# Sample players
# ===============
sample_players = [
    ("Luis", 0),
    ("Abigail", 0),
    ("Taja", 0),
    ("Jay", 0),
    ("Emma", 0)
]

cursor.executemany("""
INSERT OR IGNORE INTO players (name, score)
VALUES (?, ?)
""", sample_players)

# =========================================
# Get player IDs 
# (for demo, assign items to Luis)
# =========================================

cursor.execute("SELECT id FROM players WHERE name = ?", ("Luis",))
player_row = cursor.fetchone()
player_id = player_row[0] if player_row else 1

sample_items = [
    (player_id, "Black Beans", "Canned", 2, "2026-03-01", 1.50),
    (player_id, "Milk", "Dairy", 1, "2026-02-12", 3.25),
    (player_id, "Apples", "Produce", 5, "2026-02-15", 0.75),
    (player_id, "Bread", "Bakery", 1, "2026-02-11", 2.50),
    (player_id, "Yogurt", "Dairy", 3, "2026-02-13", 1.10),
    (player_id, "Tomatoes", "Produce", 4, "2026-02-14", 0.90)
]

cursor.executemany("""
INSERT INTO inventory (player_id, name, category, quantity, best_by, price)
VALUES (?,?,?,?,?,?)
""", sample_items)

# =========================================
# Get player IDs 
# (for demo, assign items to Abigail)
# =========================================

cursor.execute("SELECT id FROM players WHERE name = ?", ("Abigail",))
player_row = cursor.fetchone()
player_id = player_row[0] if player_row else 1

sample_items = [
    (player_id, "Black Beans", "Canned", 2, "2026-03-01", 1.50),
    (player_id, "Milk", "Dairy", 1, "2026-02-12", 3.25),
    (player_id, "Apples", "Produce", 5, "2026-02-15", 0.75),
    (player_id, "Bread", "Bakery", 1, "2026-02-11", 2.50),
    (player_id, "Yogurt", "Dairy", 3, "2026-02-13", 1.10),
    (player_id, "Tomatoes", "Produce", 4, "2026-02-14", 0.90)
]

cursor.executemany("""
INSERT INTO inventory (player_id, name, category, quantity, best_by, price)
VALUES (?,?,?,?,?,?)
""", sample_items)

# =========================================
# Get player IDs 
# (for demo, assign items to Taja)
# =========================================

cursor.execute("SELECT id FROM players WHERE name = ?", ("Taja",))
player_row = cursor.fetchone()
player_id = player_row[0] if player_row else 1

sample_items = [
    (player_id, "Black Beans", "Canned", 2, "2026-03-01", 1.50),
    (player_id, "Milk", "Dairy", 1, "2026-02-12", 3.25),
    (player_id, "Apples", "Produce", 5, "2026-02-15", 0.75),
    (player_id, "Bread", "Bakery", 1, "2026-02-11", 2.50),
    (player_id, "Yogurt", "Dairy", 3, "2026-02-13", 1.10),
    (player_id, "Tomatoes", "Produce", 4, "2026-02-14", 0.90)
]

cursor.executemany("""
INSERT INTO inventory (player_id, name, category, quantity, best_by, price)
VALUES (?,?,?,?,?,?)
""", sample_items)

# =========================================
# Get player IDs 
# (for demo, assign items to Jay)
# =========================================

cursor.execute("SELECT id FROM players WHERE name = ?", ("Jay",))
player_row = cursor.fetchone()
player_id = player_row[0] if player_row else 1

sample_items = [
    (player_id, "Black Beans", "Canned", 2, "2026-03-01", 1.50),
    (player_id, "Milk", "Dairy", 1, "2026-02-12", 3.25),
    (player_id, "Apples", "Produce", 5, "2026-02-15", 0.75),
    (player_id, "Bread", "Bakery", 1, "2026-02-11", 2.50),
    (player_id, "Yogurt", "Dairy", 3, "2026-02-13", 1.10),
    (player_id, "Tomatoes", "Produce", 4, "2026-02-14", 0.90)
]

cursor.executemany("""
INSERT INTO inventory (player_id, name, category, quantity, best_by, price)
VALUES (?,?,?,?,?,?)
""", sample_items)

# =========================================
# Get player IDs 
# (for demo, assign items to Emma)
# =========================================

cursor.execute("SELECT id FROM players WHERE name = ?", ("Emma",))
player_row = cursor.fetchone()
player_id = player_row[0] if player_row else 1

sample_items = [
    (player_id, "Black Beans", "Canned", 2, "2026-03-01", 1.50),
    (player_id, "Milk", "Dairy", 1, "2026-02-12", 3.25),
    (player_id, "Apples", "Produce", 5, "2026-02-15", 0.75),
    (player_id, "Bread", "Bakery", 1, "2026-02-11", 2.50),
    (player_id, "Yogurt", "Dairy", 3, "2026-02-13", 1.10),
    (player_id, "Tomatoes", "Produce", 4, "2026-02-14", 0.90)
]

cursor.executemany("""
INSERT INTO inventory (player_id, name, category, quantity, best_by, price)
VALUES (?,?,?,?,?,?)
""", sample_items)

conn.commit()
conn.close()