import sqlite3

# Inserts sample players and items into inventory.db
# It was helpful at the start of the site/app
# but is no longer needed

conn = sqlite3.connect("src/instance/inventory.db") # <-----  if database or tables are not found on your system check this line first
cursor = conn.cursor()

# ===============
# Sample players
# ===============
sample_players = [
    ("Luis", "Luis", "d", "d", 0)
]

cursor.executemany("""
INSERT OR IGNORE INTO players (name, username, password_hash, profile_picture, score)
VALUES (?, ?, ?, ?, ?)
""", sample_players)

# =========================================
# Get player IDs 
# (for demo, assign items to Luis)
# =========================================

cursor.execute("SELECT id FROM players WHERE name = ?", ("Luis",))
player_row = cursor.fetchone()
player_id = player_row[0] if player_row else 1

sample_items = [
#   (player_id, "name",               "category",               quantity,               unit,               "measurement_type",               quantity_grams,               quantity_ml,               "purchase_date",               "best_by", raw_meat, perishable, opened, donation_allowed, decompostion_flag,     price,      "status")
    (player_id, "Chicken Breast",         "Meat",                      2,               "lb",                         "weight",                          907,                      None,                  "2026-02-15",             "2026-02-20",        1,          1,      0,                0,                 0,     9.99,      "active"),
    (player_id, "Milk",                  "Dairy",                     16,            "fl_oz",                         "volume",                         None,                       473,                  "2026-02-10",             "2026-02-22",        0,          1,      1,                0,                 0,     3.50,      "active"),
    (player_id, "Spinach",             "Produce",                    150,                "g",                         "weight",                          150,                      None,                  "2026-02-05",             "2026-02-12",        0,          1,      0,                0,                 1,     1.99,      "active")

]

cursor.executemany("""
INSERT INTO inventory (player_id, name, category, quantity, unit, measurement_type, quantity_grams, quantity_ml, purchase_date, best_by, raw_meat, perishable, opened, donation_allowed, decomposition_flag, price, status)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", sample_items)



conn.commit()
conn.close()