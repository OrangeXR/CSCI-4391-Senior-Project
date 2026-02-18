## import sqlite3

# ===========================================
# Creates a database named inventory.db with:
# players: id, name, score
# inventory: id, player_id, name, category, 
# quantity, best_by, price, status
# ===========================================

## conn = sqlite3.connect("inventory.db")
## cursor = conn.cursor()

# ================================
# Players table (multiple players, 
# each with their own score)
# update: user = players
# ================================

## cursor.execute("""
## CREATE TABLE IF NOT EXISTS players (
##     id INTEGER PRIMARY KEY AUTOINCREMENT,
##     name TEXT NOT NULL,
##     username TEXT NOT NULL UNIQUE,
##     password_hash TEXT NOT NULL,
##     profile_picture TEXT,
##     score REAL NOT NULL DEFAULT 0
## )
## """)

# ================================================
# Inventory table (items belong to current player)
# ================================================

## cursor.execute("""
## CREATE TABLE IF NOT EXISTS inventory (
##     id INTEGER PRIMARY KEY AUTOINCREMENT,
##     player_id INTEGER NOT NULL,
##     name TEXT NOT NULL,
##     category TEXT NOT NULL,
##     quantity INTEGER NOT NULL,
##     best_by TEXT NOT NULL,
##     price REAL NOT NULL,
##    status TEXT NOT NULL DEFAULT 'active',  -- active, used, donated, composted, wasted
##     FOREIGN KEY (player_id) REFERENCES players(id)
## )
## """)
## 
## conn.commit()
## conn.close()

## ==================================================================================================================================

import sqlite3

# ===========================================
# Creates a database named inventory.db with:
# players (users): id, name, username, password_hash,
# profile_picture, score
# inventory: id, player_id, name, category,
# quantity, best_by, price, status
# ===========================================

conn = sqlite3.connect("inventory.db")
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
    best_by TEXT NOT NULL,
    price REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    FOREIGN KEY (player_id) REFERENCES players(id)
)
""")

conn.commit()
conn.close()