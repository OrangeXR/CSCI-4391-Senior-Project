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
    ("demo",   "demo", "scrypt:32768:8:1$IT3KjqtMgxIUZB1S$0cc425013292eac69df26608de00c8b9f028162d6b56ba08a16ec75e5277a3319b7d1f431f9a103527fb618bf92fc0f58f12dc51186833295cfd9284bdf99cfa",  "demo.png", "", "", 0),
    ("demo2", "demo2", "scrypt:32768:8:1$UIENB92CqyeJJyLg$1d7a6b3bd5d0bc9673627a380181e8734de2147eadb09aa3a1d16f917dd63ec1076223fd5c9d5afbade302f45683d344218659cdbb4fd10a2e45f9b1f3be2b2e", "demo2.png", "", "", 0),
    ("empty", "empty", "scrypt:32768:8:1$u2U8MGlJ2UBcGb5A$205e1984fc8f56ed7cbdfdb1fe6de9677f9339a2f553dfd38b376372ce0c97e921fa2521b4101766f1f502ef8ae040e2c50ba5c1bb2f705f852e24c1aaadb604",          "", "", "", 0)
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

cursor.execute("SELECT id FROM players WHERE name = ?", ("demo2",))
player_row = cursor.fetchone()
player_id = player_row[0] if player_row else 2

sample_items = [
#   (id,   player_id,                  "name",      "category",   quantity,      unit,      "measurement_type",   quantity_grams,   quantity_ml,     "purchase_date",    "best_by", raw_meat, perishable, opened, donation_allowed, decompostion_flag,     price,      "status")
    ( 1,            1,            'Tortilla',        'Bakery',          1,   'count',                 'count',             None,          None,        '2026-02-09', '2026-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 2,            1,                'Bread',        'Bakery',          1,    'loaf',                 'count',             None,          None,        '2026-02-10', '2026-02-14',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 3,            1,                'Sugar',        'Pantry',        500,       'g',                'weight',              500,          None,        '2026-01-12', '2028-01-12',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 4,            1,                 'Salt',        'Pantry',        250,       'g',                'weight',              250,          None,        '2026-01-10', '2028-01-10',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 5,            1,            'Olive Oil',        'Pantry',        500,      'ml',                'volume',             None,           500,        '2026-01-15', '2027-01-15',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 6,            1,         'Tomato Sauce',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-01', '2027-08-01',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 7,            1,        'Corn (Canned)',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-01', '2028-02-01',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 8,            1, 'Black Bean (Canned)',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-01', '2028-02-01',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 9,            1,                'Pasta',        'Grains',        500,       'g',                'weight',              500,          None,        '2026-01-25', '2027-01-25',        0,          1,      0,                1,                 0,         0,      'active'),
    (10,            1,                 'Rice',        'Grains',       1000,       'g',                'weight',             1000,          None,        '2026-01-20', '2027-01-20',        0,          1,      0,                1,                 0,         0,      'active'),
    (11,            1,         'Strawberry',       'Produce',        200,       'g',                'weight',              200,          None,        '2026-02-10', '2026-02-14',        0,          1,      0,                1,                 0,         0,      'active'),
    (12,            1,              'Banana',       'Produce',          4,   'count',                 'count',             None,          None,        '2026-02-09', '2026-02-15',        0,          1,      0,                1,                 0,         0,      'active'),
    (13,            1,               'Onion',       'Produce',        300,       'g',                'weight',              300,          None,        '2026-02-06', '2026-02-28',        0,          1,      0,                1,                 0,         0,      'active'),
    (14,            1,             'Potato',       'Produce',        500,       'g',                'weight',              500,          None,        '2026-02-07', '2026-02-25',        0,          1,      0,                1,                 0,         0,      'active'),
    (15,            1,              'Carrot',       'Produce',        300,       'g',                'weight',              300,          None,        '2026-02-08', '2026-02-18',        0,          1,      0,                1,                 0,         0,      'active'),
    (16,            1,         'Greek Yogurt',         'Dairy',        150,       'g',                'weight',              150,          None,        '2026-02-12', '2026-02-20',        0,          1,      0,                1,                 0,         0,      'active'),
    (17,            1,       'Cheddar Cheese',         'Dairy',        200,       'g',                'weight',              200,          None,        '2026-02-11', '2026-03-01',        0,          1,      0,                1,                 0,         0,      'active'),
    (18,            1,                 'Egg',         'Dairy',         12,   'count',                 'count',             None,          None,        '2026-02-10', '2026-03-05',        0,          1,      0,                1,                 0,         0,      'active'),
    (19,            1,           'Pork Chop',          'Meat',          2,      'lb',                'weight',             None,          None,        '2026-02-13', '2026-02-18',        1,          1,      0,                1,                 0,         0,      'active'),
    (20,            1,          'Ground Beef',          'Meat',          1,      'lb',                'weight',             None,          None,        '2026-02-14', '2026-02-19',        1,          1,      0,                1,                 0,         0,      'active'),
    (21,            1,              'Spinach',       'Produce',        100,       'g',                'weight',              100,          None,        '2026-02-05', '2026-02-12',        0,          1,      0,                1,                 0,         0,      'active'),
    (22,            1,                 'Milk',         'Dairy',         16,   'fl_oz',                'volume',             None,            16,        '2026-02-10', '2026-02-22',        0,          1,      0,                1,                 0,         0,      'active'),
    (23,            1,       'Chicken Breast',          'Meat',          2,      'lb',                'weight',             None,          None,        '2026-02-15', '2026-02-20',        1,          1,      0,                1,                 0,         0,      'active'),
    (24,            1,      'Parmesan Cheese',         'Dairy',        200,       'g',                'weight',              200,          None,        '2026-02-20', '2026-04-20',        0,          1,      0,                1,                 0,         0,      'active'),
    (25,            1,    'Mozzarella Cheese',         'Dairy',        250,       'g',                'weight',              250,          None,        '2026-02-20', '2026-03-10',        0,          1,      0,                1,                 0,         0,      'active'),
    (26,            1,       'Ricotta Cheese',         'Dairy',        200,       'g',                'weight',              200,          None,        '2026-02-20', '2026-03-05',        0,          1,      0,                1,                 0,         0,      'active'),
    (27,            1,        'Basil (Fresh)',       'Produce',         30,       'g',                'weight',               30,          None,        '2026-02-20', '2026-02-27',        0,          1,      0,                1,                 0,         0,      'active'),
    (28,            1,      'Oregano (Dried)',        'Pantry',         20,       'g',                'weight',               20,          None,        '2026-02-20', '2028-02-20',        0,          0,      0,                1,                 0,         0,      'active'),
    (29,            1,        'Thyme (Dried)',        'Pantry',         20,       'g',                'weight',               20,          None,        '2026-02-20', '2028-02-20',        0,          0,      0,                1,                 0,         0,      'active'),
    (30,            1,               'Garlic',       'Produce',        100,       'g',                'weight',              100,          None,        '2026-02-20', '2026-03-15',        0,          1,      0,                1,                 0,         0,      'active'),
    (31,            1,     'Crushed Tomato',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-20', '2028-02-20',        0,          1,      0,                1,                 0,         0,      'active'),
    (32,            1,         'Tomato Paste',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-20', '2028-02-20',        0,          1,      0,                1,                 0,         0,      'active'),
    (33,            1,          'Pesto Sauce',        'Pantry',        200,       'g',                'weight',              200,          None,        '2026-02-20', '2027-02-20',        0,          1,      0,                1,                 0,         0,      'active'),
    (34,            1,     'Balsamic Vinegar',        'Pantry',        250,      'ml',                'volume',             None,           250,        '2026-02-20', '2028-02-20',        0,          0,      0,                1,                 0,         0,      'active'),
    (35,            1,     'Red Wine Vinegar',        'Pantry',        250,      'ml',                'volume',             None,           250,        '2026-02-20', '2028-02-20',        0,          0,      0,                1,                 0,         0,      'active'),
    (36,            1,            'Spaghetti',        'Grains',        500,       'g',                'weight',              500,          None,        '2026-02-20', '2027-02-20',        0,          0,      0,                1,                 0,         0,      'active'),
    (37,            1,           'Fettuccine',        'Grains',        500,       'g',                'weight',              500,          None,        '2026-02-20', '2027-02-20',        0,          0,      0,                1,                 0,         0,      'active'),
    (38,            1,          'Penne Pasta',        'Grains',        500,       'g',                'weight',              500,          None,        '2026-02-20', '2027-02-20',        0,          0,      0,                1,                 0,         0,      'active'),
    (39,            1,         'Arborio Rice',        'Grains',        500,       'g',                'weight',              500,          None,        '2026-02-20', '2027-02-20',        0,          0,      0,                1,                 0,         0,      'active'),
    (40,            1,   'Polenta (Cornmeal)',        'Grains',        500,       'g',                'weight',              500,          None,        '2026-02-20', '2027-02-20',        0,          0,      0,                1,                 0,         0,      'active'),
    (41,            1,      'Italian Sausage',          'Meat',          1,      'lb',                'weight',             None,          None,        '2026-02-20', '2026-02-25',        1,          1,      0,                1,                 0,         0,      'active'),
    (42,            1,           'Prosciutto',          'Meat',        150,       'g',                'weight',              150,          None,        '2026-02-20', '2026-03-05',        1,          1,      0,                1,                 0,         0,      'active'),
    (43,            1,               'Salami',          'Meat',        200,       'g',                'weight',              200,          None,        '2026-02-20', '2026-03-10',        1,          1,      0,                1,                 0,         0,      'active'),
    (44,            1,            'Anchovy',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-20', '2028-02-20',        0,          1,      0,                1,                 0,         0,      'active'),
    (45,            1,               'Caper',        'Pantry',        100,       'g',                'weight',              100,          None,        '2026-02-20', '2027-02-20',        0,          0,      0,                1,                 0,         0,      'active'),
    (46,            1,   'Sun-Dried Tomato',        'Pantry',        150,       'g',                'weight',              150,          None,        '2026-02-20', '2027-02-20',        0,          0,      0,                1,                 0,         0,      'active'),
    (47,            1,     'Artichoke Heart',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-20', '2028-02-20',        0,          1,      0,                1,                 0,         0,      'active'),
    (48,            1,            'Mushroom',       'Produce',        200,       'g',                'weight',              200,          None,        '2026-02-20', '2026-02-27',        0,          1,      0,                1,                 0,         0,      'active'),
    (49,            1,             'Zucchini',       'Produce',        300,       'g',                'weight',              300,          None,        '2026-02-20', '2026-03-05',        0,          1,      0,                1,                 0,         0,      'active'),
    (50,            1,             'Eggplant',       'Produce',        400,       'g',                'weight',              400,          None,        '2026-02-20', '2026-03-05',        0,          1,      0,                1,                 0,         0,      'active'),
    (51,            1,    'Red Pepper Flake',        'Pantry',         20,       'g',                'weight',               20,          None,        '2026-02-20', '2028-02-20',        0,          0,      0,                1,                 0,         0,      'active'),
    (52,            1, 'Italian Bread Crumb',        'Pantry',        300,       'g',                'weight',              300,          None,        '2026-02-20', '2027-02-20',        0,          0,      0,                1,                 0,         0,      'active'),
    (53,            1,           'Mascarpone',         'Dairy',        200,       'g',                'weight',              200,          None,        '2026-02-20', '2026-03-05',        0,          1,      0,                1,                 0,         0,      'active'),
    (54,            1, 'Pinto Bean (Canned)',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-20', '2028-02-20',        0,          1,      0,                1,                 0,         0,      'active'),
    (55,            1,        'Refried Bean',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-20', '2028-02-20',        0,          1,      0,                1,                 0,         0,      'active'),
    (56,            1,   'Jalapeño (Canned)',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-20', '2028-02-20',        0,          1,      0,                1,                 0,         0,      'active'),
    (57,            1,'Chipotle Peppers in Adobo',    'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-20', '2028-02-20',        0,          1,      0,                1,                 0,         0,      'active'),
    (58,            1,             'Cilantro',       'Produce',         30,       'g',                'weight',               30,          None,        '2026-02-20', '2026-02-27',        0,          1,      0,                1,                 0,         0,      'active'),
    (59,            1,                'Lime',       'Produce',          4,   'count',                 'count',             None,          None,        '2026-02-20', '2026-03-01',        0,          1,      0,                1,                 0,         0,      'active'),
    (60,            1,             'Avocado',       'Produce',          2,   'count',                 'count',             None,          None,        '2026-02-20', '2026-02-27',        0,          1,      0,                1,                 0,         0,      'active'),
    (61,            1,         'Queso Fresco',         'Dairy',        200,       'g',                'weight',              200,          None,        '2026-02-20', '2026-03-05',        0,          1,      0,                1,                 0,         0,      'active'),
    (62,            1,              'Chorizo',          'Meat',          1,      'lb',                'weight',             None,          None,        '2026-02-20', '2026-02-25',        1,          1,      0,                1,                 0,         0,      'active'),
    (63,            1,  'Corn Tortilla Chip',         'Snack',        300,       'g',                'weight',              300,          None,        '2026-02-20', '2027-02-20',        0,          0,      0,                1,                 0,         0,      'active')
]


sample_items_2 = [
    (64,             2,             'Bagel',         'Bakery',          1,      'pack',               'count',             None,          None,        '2026-02-10', '2026-02-18',         0,         1,     0,                 1,                 0,         0,         'active'),
    (65,             2,             'Cereal',         'Pantry',        300,         'g',              'weight',              300,          None,        '2026-01-20', '2027-01-20',         0,         1,     0,                 1,                 0,         0,         'active'),
    (66,             2,        'Apple Juice',       'Beverage',         32,     'fl_oz',              'volume',             None,            32,        '2026-02-05', '2026-03-05',         0,         1,     0,                 1,                 0,         0,         'active'),
    (67,             2,     'Chicken Thigh',           'Meat',          2,        'lb',              'weight',             None,          None,        '2026-02-14', '2026-02-19',         1,         1,     0,                 1,                 0,         0,         'active'),
    (68,             2,            'Lettuce',        'Produce',        150,         'g',              'weight',              150,          None,        '2026-02-09', '2026-02-15',         0,         1,     0,                 1,                 0,         0,         'active')

]





cursor.executemany("""
INSERT INTO inventory (id,player_id, name, category, quantity, unit, measurement_type, quantity_grams, quantity_ml, purchase_date, best_by, raw_meat, perishable, opened, donation_allowed, decomposition_flag, price, status)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", sample_items)

cursor.executemany("""
INSERT OR IGNORE INTO inventory (id, player_id, name, category, quantity, unit, measurement_type, quantity_grams, quantity_ml, purchase_date, best_by, raw_meat, perishable, opened, donation_allowed, decomposition_flag, price, status)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", sample_items_2)


conn.commit()
conn.close()


