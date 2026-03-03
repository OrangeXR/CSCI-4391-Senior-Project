import sqlite3

# ===========================================
# Creates a database named inventory.db with:
# players (users): id, name, username, password_hash,
# profile_picture, score
# inventory: id, player_id, name, category,
# quantity, best_by, price, status
# ===========================================

conn = sqlite3.connect("src/instance/inventory.db") # <------- Moved ail files into src as per professor
cursor = conn.cursor()

# ================================
# Players table (users = players)
# ================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    profile_picture TEXT,
    food_allergies TEXT "", 
    dietary_needs TEXT "",
    score REAL NOT NULL DEFAULT 0
)
""")

# ================================================
# Inventory table (items belong to current player)
# ================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit TEXT NOT NULL,
    measurement_type TEXT NOT NULL,
    quantity_grams REAL,
    quantity_ml REAL,
    purchase_date TEXT,
    best_by TEXT NOT NULL,
    raw_meat BOOLEAN DEFAULT 0,
    perishable BOOLEAN DEFAULT 1,
    opened BOOLEAN DEFAULT 0,
    donation_allowed BOOLEAN DEFAULT 1,
    decomposition_flag BOOLEAN DEFAULT 0,
    price REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    FOREIGN KEY (player_id) REFERENCES players(id)
)
""")


# ================================================
# Meals table (items belong to current player)
# ================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id)
)
""")



conn.commit()
conn.close()
