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
    ("demo", "demo", "scrypt:32768:8:1$IT3KjqtMgxIUZB1S$0cc425013292eac69df26608de00c8b9f028162d6b56ba08a16ec75e5277a3319b7d1f431f9a103527fb618bf92fc0f58f12dc51186833295cfd9284bdf99cfa", "10685419_10152507377767056_9098428566776341261_n.jpg", 0)
]

cursor.executemany("""
INSERT OR IGNORE INTO players (name, username, password_hash, profile_picture, score)
VALUES (?, ?, ?, ?, ?)
""", sample_players)

# =========================================
# Get player IDs 
# (for demo, assign items to Luis)
# =========================================

cursor.execute("SELECT id FROM players WHERE name = ?", ("demo",))
player_row = cursor.fetchone()
player_id = player_row[0] if player_row else 1

sample_items = [
#   (player_id, "name",               "category",               quantity,               unit,               "measurement_type",               quantity_grams,               quantity_ml,               "purchase_date",               "best_by", raw_meat, perishable, opened, donation_allowed, decompostion_flag,     price,      "status")
    (player_id, "Chicken Breast",         "Meat",                      2,               "lb",                         "weight",                          907,                      None,                  "2026-02-15",             "2026-02-20",        1,          1,      0,                0,                 0,     9.99,      "active"),
    (player_id, "Milk",                  "Dairy",                     16,            "fl_oz",                         "volume",                         None,                       473,                  "2026-02-10",             "2026-02-22",        0,          1,      1,                0,                 0,     3.50,      "active"),
    (player_id, "Spinach",             "Produce",                    150,                "g",                         "weight",                          150,                      None,                  "2026-02-05",             "2026-02-12",        0,          1,      0,                0,                 1,     1.99,      "active"),
    (player_id, "Ground Beef",            "Meat",                      1,               "lb",                         "weight",                          454,                      None,                  "2026-02-14",             "2026-02-19",        1,          1,      0,                0,                 0,     6.49,      "active"),
    (player_id, "Pork Chops",             "Meat",                      2,               "lb",                         "weight",                          907,                      None,                  "2026-02-13",             "2026-02-18",        1,          1,      0,                0,                 0,     8.99,      "active"),
    (player_id, "Eggs",                  "Dairy",                     12,            "count",                          "count",                         None,                      None,                  "2026-02-10",             "2026-03-05",        0,          1,      0,                0,                 0,     2.99,      "active"),
    (player_id, "Cheddar Cheese",        "Dairy",                    200,                "g",                         "weight",                          200,                      None,                  "2026-02-11",             "2026-03-01",        0,          1,      0,                0,                 0,     4.50,      "active"),
    (player_id, "Greek Yogurt",          "Dairy",                    150,                "g",                         "weight",                          150,                      None,                  "2026-02-12",             "2026-02-20",        0,          1,      0,                0,                 0,     1.25,      "active"),
    (player_id, "Carrots",             "Produce",                    300,                "g",                         "weight",                          300,                      None,                  "2026-02-08",             "2026-02-18",        0,          1,      0,                0,                 1,     1.99,      "active"),
    (player_id, "Potatoes",            "Produce",                    500,                "g",                         "weight",                          500,                      None,                  "2026-02-07",             "2026-02-25",        0,          1,      0,                0,                 1,     2.49,      "active"),
    (player_id, "Onions",              "Produce",                    200,                "g",                         "weight",                          200,                      None,                  "2026-02-06",             "2026-02-28",        0,          1,      0,                0,                 1,     1.29,      "active"),
    (player_id, "Bananas",             "Produce",                      4,            "count",                          "count",                         None,                      None,                  "2026-02-09",             "2026-02-15",        0,          1,      0,                0,                 1,     1.10,      "active"),
    (player_id, "Strawberries",        "Produce",                    250,                "g",                         "weight",                          250,                      None,                  "2026-02-10",             "2026-02-14",        0,          1,      0,                0,                 1,     3.99,      "active"),
    (player_id, "Rice",                 "Grains",                   1000,                "g",                         "weight",                         1000,                      None,                  "2026-01-20",             "2027-01-20",        0,          0,      0,                1,                 0,     2.99,      "active"),
    (player_id, "Pasta",                "Grains",                    500,                "g",                         "weight",                          500,                      None,                  "2026-01-25",             "2027-01-25",        0,          0,      0,                1,                 0,     1.79,      "active"),
    (player_id, "Black Beans (Canned)", "Canned",                      1,              "can",                          "count",                         None,                      None,                  "2026-02-01",             "2028-02-01",        0,          0,      0,                1,                 0,     1.29,      "active"),
    (player_id, "Corn (Canned)",        "Canned",                      1,              "can",                          "count",                         None,                      None,                  "2026-02-01",             "2028-02-01",        0,          0,      0,                1,                 0,     1.19,      "active"),
    (player_id, "Tomato Sauce",         "Canned",                      1,              "can",                          "count",                         None,                      None,                  "2026-02-01",             "2027-08-01",        0,          0,      0,                1,                 0,     1.49,      "active"),
    (player_id, "Olive Oil",            "Pantry",                    500,               "ml",                         "volume",                         None,                       500,                  "2026-01-15",             "2027-01-15",        0,          0,      0,                1,                 0,     6.99,      "active"),
    (player_id, "Salt",                 "Pantry",                    250,                "g",                         "weight",                          250,                      None,                  "2026-01-10",             "2028-01-10",        0,          0,      0,                1,                 0,     0.99,      "active"),
    (player_id, "Sugar",                "Pantry",                    500,                "g",                         "weight",                          500,                      None,                  "2026-01-12",             "2028-01-12",        0,          0,      0,                1,                 0,     1.49,      "active"),
    (player_id, "Bread",                "Bakery",                      1,             "loaf",                          "count",                         None,                      None,                  "2026-02-10",             "2026-02-14",        0,          1,      0,                0,                 1,     2.99,      "active"),
    (player_id, "Tortillas",            "Bakery",                     10,            "count",                          "count",                         None,                      None,                  "2026-02-09",             "2026-02-16",        0,          1,      0,                0,                 1,     2.49,      "active")
]


cursor.executemany("""
INSERT INTO inventory (player_id, name, category, quantity, unit, measurement_type, quantity_grams, quantity_ml, purchase_date, best_by, raw_meat, perishable, opened, donation_allowed, decomposition_flag, price, status)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", sample_items)



conn.commit()
conn.close()