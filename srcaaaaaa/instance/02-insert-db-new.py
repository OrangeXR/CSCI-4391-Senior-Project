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
    ("demo", "demo", "scrypt:32768:8:1$IT3KjqtMgxIUZB1S$0cc425013292eac69df26608de00c8b9f028162d6b56ba08a16ec75e5277a3319b7d1f431f9a103527fb618bf92fc0f58f12dc51186833295cfd9284bdf99cfa", "demo.png", "", "", 0)
]

cursor.executemany("""
INSERT OR IGNORE INTO players (name, username, password_hash, profile_picture, food_allergies, dietary_needs, score)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", sample_players)

# =========================================
# Get player IDs 
# (for demo, assign items to Luis)
# =========================================

cursor.execute("SELECT id FROM players WHERE name = ?", ("demo",))
player_row = cursor.fetchone()
player_id = player_row[0] if player_row else 1

sample_items = [
#   (id,   player_id,                  "name",      "category",   quantity,      unit,      "measurement_type",   quantity_grams,   quantity_ml,     "purchase_date",    "best_by", raw_meat, perishable, opened, donation_allowed, decompostion_flag,     price,      "status")
    ( 1,            1,            'Tortillas',        'Bakery',          1,   'count',                 'count',             None,          None,        '2026-02-09', '2026-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 2,            1,                'Bread',        'Bakery',          1,    'loaf',                 'count',             None,          None,        '2026-02-10', '2026-02-14',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 3,            1,                'Sugar',        'Pantry',        500,       'g',                'weight',              500,          None,        '2026-01-12', '2028-01-12',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 4,            1,                 'Salt',        'Pantry',        250,       'g',                'weight',              250,          None,        '2026-01-10', '2028-01-10',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 5,            1,            'Olive Oil',        'Pantry',        500,      'ml',                'volume',             None,           500,        '2026-01-15', '2027-01-15',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 6,            1,         'Tomato Sauce',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-01', '2027-08-01',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 7,            1,        'Corn (Canned)',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-01', '2028-02-01',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 8,            1, 'Black Beans (Canned)',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-01', '2028-02-01',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 9,            1,                'Pasta',        'Grains',        500,       'g',                'weight',              500,          None,        '2026-01-25', '2027-01-25',        0,          1,      0,                1,                 0,         0,      'active'),
    (10,            1,                 'Rice',        'Grains',       1000,       'g',                'weight',             1000,          None,        '2026-01-20', '2027-01-20',        0,          1,      0,                1,                 0,         0,      'active'),
    (11,            1,         'Strawberries',       'Produce',        200,       'g',                'weight',              200,          None,        '2026-02-10', '2026-02-14',        0,          1,      0,                1,                 0,         0,      'active'),
    (12,            1,              'Bananas',       'Produce',          4,   'count',                 'count',             None,          None,        '2026-02-09', '2026-02-15',        0,          1,      0,                1,                 0,         0,      'active'),
    (13,            1,               'Onions',       'Produce',        300,       'g',                'weight',              300,          None,        '2026-02-06', '2026-02-28',        0,          1,      0,                1,                 0,         0,      'active'),
    (14,            1,             'Potatoes',       'Produce',        500,       'g',                'weight',              500,          None,        '2026-02-07', '2026-02-25',        0,          1,      0,                1,                 0,         0,      'active'),
    (15,            1,              'Carrots',       'Produce',        300,       'g',                'weight',              300,          None,        '2026-02-08', '2026-02-18',        0,          1,      0,                1,                 0,         0,      'active'),
    (16,            1,         'Greek Yogurt',         'Dairy',        150,       'g',                'weight',              150,          None,        '2026-02-12', '2026-02-20',        0,          1,      0,                1,                 0,         0,      'active'),
    (17,            1,       'Cheddar Cheese',         'Dairy',        200,       'g',                'weight',              200,          None,        '2026-02-11', '2026-03-01',        0,          1,      0,                1,                 0,         0,      'active'),
    (18,            1,                 'Eggs',         'Dairy',         12,   'count',                 'count',             None,          None,        '2026-02-10', '2026-03-05',        0,          1,      0,                1,                 0,         0,      'active'),
    (19,            1,           'Pork Chops',          'Meat',          2,      'lb',                'weight',             None,          None,        '2026-02-13', '2026-02-18',        1,          1,      0,                1,                 0,         0,      'active'),
    (20,            1,          'Ground Beef',          'Meat',          1,      'lb',                'weight',             None,          None,        '2026-02-14', '2026-02-19',        1,          1,      0,                1,                 0,         0,      'active'),
    (21,            1,              'Spinach',       'Produce',        100,       'g',                'weight',              100,          None,        '2026-02-05', '2026-02-12',        0,          1,      0,                1,                 0,         0,      'active'),
    (22,            1,                 'Milk',         'Dairy',         16,   'fl_oz',                'volume',             None,            16,        '2026-02-10', '2026-02-22',        0,          1,      0,                1,                 0,         0,      'active'),
    (23,            1,       'Chicken Breast',          'Meat',          2,      'lb',                'weight',             None,          None,        '2026-02-15', '2026-02-20',        1,          1,      0,                1,                 0,         0,      'active')



]

cursor.executemany("""
INSERT INTO inventory (id,player_id, name, category, quantity, unit, measurement_type, quantity_grams, quantity_ml, purchase_date, best_by, raw_meat, perishable, opened, donation_allowed, decomposition_flag, price, status)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", sample_items)



conn.commit()
conn.close()
