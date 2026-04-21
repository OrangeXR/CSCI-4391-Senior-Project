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
    ("empty", "empty", "scrypt:32768:8:1$u2U8MGlJ2UBcGb5A$205e1984fc8f56ed7cbdfdb1fe6de9677f9339a2f553dfd38b376372ce0c97e921fa2521b4101766f1f502ef8ae040e2c50ba5c1bb2f705f852e24c1aaadb604",          "", "", "", 0),
    ("expired", "expired", "scrypt:32768:8:1$EIrxLnJwbD3BcyC7$dc371a16a70728f7c6db5d7306571d6e8a32a9f1cc3400b706318175c9e86d8f4a51253546633b3c012af7b3aadda96971d1b313de9cb1b8f9e02a45238f11cb",      "", "", "", 0),
    ("vegetarian", "vegetarian", "scrypt:32768:8:1$fkDeFCRZuUv5zMjo$33dba63e1b30af358748feafbb29b9d2a169dd416f3639ec5fae39756b9f99aacf566ea25f93f38f53c19caaee9aa85294465a77f5135a9cee1ecc24a8763b65",      "", "", "vegetarian", 0)

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

cursor.execute("SELECT id FROM players WHERE name = ?", ("empty",))
player_row = cursor.fetchone()
player_id = player_row[0] if player_row else 3

cursor.execute("SELECT id FROM players WHERE name = ?", ("expired",))
player_row = cursor.fetchone()
player_id = player_row[0] if player_row else 4

cursor.execute("SELECT id FROM players WHERE name = ?", ("vegetarian",))
player_row = cursor.fetchone()
player_id = player_row[0] if player_row else 5

sample_items = [
#   (id,   player_id,                  "name",      "category",   quantity,      unit,      "measurement_type",   quantity_grams,   quantity_ml,     "purchase_date",    "best_by", raw_meat, perishable, opened, donation_allowed, decompostion_flag,     price,      "status")
    ( 1,            1,            'Tortilla',        'Bakery',          1,   'count',                 'count',             None,          None,        '2026-02-09', '2026-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 2,            1,                'Bread',        'Bakery',          1,    'loaf',                 'count',             None,          None,        '2026-02-10', '2026-02-14',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 3,            1,                'Sugar',        'Pantry',        500,       'g',                'weight',              500,          None,        '2026-01-12', '2028-01-12',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 4,            1,                 'Salt',        'Pantry',        250,       'g',                'weight',              250,          None,        '2026-01-10', '2028-01-10',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 5,            1,            'Olive Oil',        'Pantry',        500,      'ml',                'volume',             None,           500,        '2026-01-15', '2027-01-15',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 6,            1,         'Tomato Sauce',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-01', '2026-04-17',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 7,            1,        'Corn (Canned)',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-01', '2026-04-17',        0,          1,      0,                1,                 0,         0,      'active'),
    ( 8,            1, 'Black Bean (Canned)',        'Canned',          1,     'can',                 'count',             None,          None,        '2026-02-01', '2026-04-17',        0,          1,      0,                1,                 0,         0,      'active'),
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


sample_items_3 = [
    
]



sample_items_4 = [
#   (id,   player_id,                  "name",      "category",   quantity,      unit,      "measurement_type",   quantity_grams,   quantity_ml,     "purchase_date",    "best_by", raw_meat, perishable, opened, donation_allowed, decompostion_flag,     price,      "status")
    (69,            4,            'Tortilla',        'Bakery',          1,   'count',                 'count',             None,          None,        '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (70,            4,                'Bread',        'Bakery',          1,    'loaf',                 'count',             None,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (71,            4,                'Sugar',        'Pantry',        500,       'g',                'weight',              500,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (72,            4,                 'Salt',        'Pantry',        250,       'g',                'weight',              250,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (73,            4,            'Olive Oil',        'Pantry',        500,      'ml',                'volume',             None,           500,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (74,            4,         'Tomato Sauce',        'Canned',          1,     'can',                 'count',             None,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (75,            4,        'Corn (Canned)',        'Canned',          1,     'can',                 'count',             None,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (76,            4, 'Black Bean (Canned)',        'Canned',          1,     'can',                 'count',             None,          None,        '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (77,            4,                'Pasta',        'Grains',        500,       'g',                'weight',              500,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (78,            4,                 'Rice',        'Grains',       1000,       'g',                'weight',             1000,          None,       '2026-01-20', '2027-01-20',        0,          1,      0,                1,                 0,         0,      'active'),
    (79,            4,         'Strawberry',       'Produce',        200,       'g',                'weight',              200,          None,         '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (80,            4,              'Banana',       'Produce',          4,   'count',                 'count',             None,          None,        '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (81,            4,               'Onion',       'Produce',        300,       'g',                'weight',              300,          None,        '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (82,            4,             'Potato',       'Produce',        500,       'g',                'weight',              500,          None,         '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (83,            4,              'Carrot',       'Produce',        300,       'g',                'weight',              300,          None,        '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (84,            4,         'Greek Yogurt',         'Dairy',        150,       'g',                'weight',              150,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (85,            4,       'Cheddar Cheese',         'Dairy',        200,       'g',                'weight',              200,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (86,            4,                 'Egg',         'Dairy',         12,   'count',                 'count',             None,          None,        '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (87,            4,           'Pork Chop',          'Meat',          2,      'lb',                'weight',             None,          None,        '2025-02-09', '2025-02-16',        1,          1,      0,                1,                 0,         0,      'active'),
    (88,            4,          'Ground Beef',          'Meat',          1,      'lb',                'weight',             None,          None,       '2025-02-09', '2025-02-16',        1,          1,      0,                1,                 0,         0,      'active'),
    (89,            4,              'Spinach',       'Produce',        100,       'g',                'weight',              100,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (90,            4,                 'Milk',         'Dairy',         16,   'fl_oz',                'volume',             None,            16,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (91,            4,       'Chicken Breast',          'Meat',          2,      'lb',                'weight',             None,          None,       '2025-02-09', '2025-02-16',        1,          1,      0,                1,                 0,         0,      'active'),
    (92,            4,      'Parmesan Cheese',         'Dairy',        200,       'g',                'weight',              200,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (93,            4,    'Mozzarella Cheese',         'Dairy',        250,       'g',                'weight',              250,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (94,            4,       'Ricotta Cheese',         'Dairy',        200,       'g',                'weight',              200,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (95,            4,        'Basil (Fresh)',       'Produce',         30,       'g',                'weight',               30,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (96,            4,      'Oregano (Dried)',        'Pantry',         20,       'g',                'weight',               20,          None,       '2025-02-09', '2025-02-16',        0,          0,      0,                1,                 0,         0,      'active'),
    (97,            4,        'Thyme (Dried)',        'Pantry',         20,       'g',                'weight',               20,          None,       '2025-02-09', '2025-02-16',        0,          0,      0,                1,                 0,         0,      'active'),
    (98,            4,               'Garlic',       'Produce',        100,       'g',                'weight',              100,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (99,            4,       'Crushed Tomato',        'Canned',          1,     'can',                 'count',             None,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (100,           4,         'Tomato Paste',        'Canned',          1,     'can',                 'count',             None,          None,      '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (101,           4,          'Pesto Sauce',        'Pantry',        200,       'g',                'weight',              200,          None,      '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (102,           4,     'Balsamic Vinegar',        'Pantry',        250,      'ml',                'volume',             None,           250,      '2025-02-09', '2025-02-16',        0,          0,      0,                1,                 0,         0,      'active'),
    (103,           4,     'Red Wine Vinegar',        'Pantry',        250,      'ml',                'volume',             None,           250,      '2025-02-09', '2025-02-16',        0,          0,      0,                1,                 0,         0,      'active'),
    (104,           4,            'Spaghetti',        'Grains',        500,       'g',                'weight',              500,          None,      '2025-02-09', '2025-02-16',        0,          0,      0,                1,                 0,         0,      'active'),
    (105,           4,           'Fettuccine',        'Grains',        500,       'g',                'weight',              500,          None,      '2025-02-09', '2025-02-16',        0,          0,      0,                1,                 0,         0,      'active'),
    (106,           4,          'Penne Pasta',        'Grains',        500,       'g',                'weight',              500,          None,      '2025-02-09', '2025-02-16',        0,          0,      0,                1,                 0,         0,      'active'),
    (107,           4,         'Arborio Rice',        'Grains',        500,       'g',                'weight',              500,          None,      '2025-02-09', '2025-02-16',        0,          0,      0,                1,                 0,         0,      'active'),
    (108,           4,   'Polenta (Cornmeal)',        'Grains',        500,       'g',                'weight',              500,          None,      '2025-02-09', '2025-02-16',        0,          0,      0,                1,                 0,         0,      'active'),
    (109,           4,      'Italian Sausage',          'Meat',          1,      'lb',                'weight',             None,          None,      '2025-02-09', '2025-02-16',        1,          1,      0,                1,                 0,         0,      'active'),
    (110,           4,           'Prosciutto',          'Meat',        150,       'g',                'weight',              150,          None,      '2026-02-20', '2026-03-05',        1,          1,      0,                1,                 0,         0,      'active'),
    (111,           4,               'Salami',          'Meat',        200,       'g',                'weight',              200,          None,      '2025-02-09', '2025-02-16',        1,          1,      0,                1,                 0,         0,      'active'),
    (112,           4,              'Anchovy',        'Canned',          1,     'can',                 'count',             None,          None,        '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (113,           4,                'Caper',        'Pantry',        100,       'g',                'weight',              100,          None,       '2025-02-09', '2025-02-16',        0,          0,      0,                1,                 0,         0,      'active'),
    (114,           4,     'Sun-Dried Tomato',        'Pantry',        150,       'g',                'weight',              150,          None,        '2026-02-20', '2027-02-20',        0,          0,      0,                1,                 0,         0,      'active'),
    (115,           4,      'Artichoke Heart',        'Canned',          1,     'can',                 'count',             None,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (116,           4,             'Mushroom',       'Produce',        200,       'g',                'weight',              200,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (117,           4,             'Zucchini',       'Produce',        300,       'g',                'weight',              300,          None,      '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (118,           4,             'Eggplant',       'Produce',        400,       'g',                'weight',              400,          None,      '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (119,           4,     'Red Pepper Flake',        'Pantry',         20,       'g',                'weight',               20,          None,       '2025-02-09', '2025-02-16',        0,          0,      0,                1,                 0,         0,      'active'),
    (120,           4,  'Italian Bread Crumb',        'Pantry',        300,       'g',                'weight',              300,          None,       '2025-02-09', '2025-02-16',        0,          0,      0,                1,                 0,         0,      'active'),
    (121,           4,           'Mascarpone',         'Dairy',        200,       'g',                'weight',              200,          None,      '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (122,           4,  'Pinto Bean (Canned)',        'Canned',          1,     'can',                 'count',             None,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (123,           4,         'Refried Bean',        'Canned',          1,     'can',                 'count',             None,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (124,           4,    'Jalapeño (Canned)',        'Canned',          1,     'can',                 'count',             None,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (125,           4,'Chipotle Peppers in Adobo',    'Canned',          1,     'can',                 'count',             None,          None,      '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (126,           4,             'Cilantro',       'Produce',         30,       'g',                'weight',               30,          None,      '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (127,           4,                 'Lime',       'Produce',          4,   'count',                 'count',             None,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (128,           4,              'Avocado',       'Produce',          2,   'count',                 'count',             None,          None,       '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (129,           4,         'Queso Fresco',         'Dairy',        200,       'g',                'weight',              200,          None,      '2025-02-09', '2025-02-16',        0,          1,      0,                1,                 0,         0,      'active'),
    (130,           4,              'Chorizo',          'Meat',          1,      'lb',                'weight',             None,          None,      '2025-02-09', '2025-02-16',        1,          1,      0,                1,                 0,         0,      'active'),
    (131,           4,   'Corn Tortilla Chip',         'Snack',        300,       'g',                'weight',              300,          None,       '2025-02-09', '2025-02-16',        0,          0,      0,                1,                 0,         0,      'active')

]


sample_items_5 = [
    (132,           5,              'Tortilla',       'Bakery',          1,    'count',                 'count',            None,          None,      '2026-02-09',   '2026-02-16',       0,        1,      0,             1,                  0,              0,      'active'),
    (133,           5,                  'Bread',             'Bakery',   1,   'loaf',  'count', None, None, '2026-02-10', '2026-02-14', 0, 1, 0, 1, 0, 0, 'active'),
    (134,           5,                  'Sugar',             'Pantry', 500,   'g',     'weight', 500, None, '2026-01-12', '2028-01-12', 0, 1, 0, 1, 0, 0, 'active'),
    (135,           5,                  'Salt',              'Pantry', 250,   'g',     'weight', 250, None, '2026-01-10', '2028-01-10', 0, 1, 0, 1, 0, 0, 'active'),
    (136,           5,              'Olive Oil',         'Pantry', 500,   'ml',    'volume', None, 500, '2026-01-15', '2027-01-15', 0, 1, 0, 1, 0, 0, 'active'),
    (137,           5,          'Tomato Sauce',      'Canned',   1,   'can',   'count', None, None, '2026-02-01', '2027-08-01', 0, 1, 0, 1, 0, 0, 'active'),
    (138,           5,          'Corn (Canned)',     'Canned',   1,   'can',   'count', None, None, '2026-02-01', '2028-02-01', 0, 1, 0, 1, 0, 0, 'active'),
    (139,           5,    'Black Bean (Canned)', 'Canned', 1,   'can',   'count', None, None, '2026-02-01', '2028-02-01', 0, 1, 0, 1, 0, 0, 'active'),
    (140,           5,                  'Pasta',             'Grains', 500,   'g',     'weight', 500, None, '2026-01-25', '2027-01-25', 0, 1, 0, 1, 0, 0, 'active'),
    (141,           5,                  'Rice',              'Grains',1000,   'g',     'weight',1000, None, '2026-01-20', '2027-01-20', 0, 1, 0, 1, 0, 0, 'active'),
    (142,           5,              'Strawberry',        'Produce',200,   'g',     'weight', 200, None, '2026-02-10', '2026-02-14', 0, 1, 0, 1, 0, 0, 'active'),
    (143,           5,                  'Banana',            'Produce',  4,   'count', 'count', None, None, '2026-02-09', '2026-02-15', 0, 1, 0, 1, 0, 0, 'active'),
    (144,           5,                  'Onion',             'Produce',300,   'g',     'weight', 300, None, '2026-02-06', '2026-02-28', 0, 1, 0, 1, 0, 0, 'active'),
    (145,           5,                  'Potato',            'Produce',500,   'g',     'weight', 500, None, '2026-02-07', '2026-02-25', 0, 1, 0, 1, 0, 0, 'active'),
    (146,           5,                  'Carrot',            'Produce',300,   'g',     'weight', 300, None, '2026-02-08', '2026-02-18', 0, 1, 0, 1, 0, 0, 'active'),
    (147,           5,              'Greek Yogurt',      'Dairy',  150,   'g',     'weight', 150, None, '2026-02-12', '2026-02-20', 0, 1, 0, 1, 0, 0, 'active'),
    (148,           5,          'Cheddar Cheese',    'Dairy',  200,   'g',     'weight', 200, None, '2026-02-11', '2026-03-01', 0, 1, 0, 1, 0, 0, 'active'),
    (149,           5,                  'Egg',               'Dairy',   12,   'count', 'count', None, None, '2026-02-10', '2026-03-05', 0, 1, 0, 1, 0, 0, 'active'),
    (150,           5,                  'Spinach',           'Produce',100,   'g',     'weight', 100, None, '2026-02-05', '2026-02-12', 0, 1, 0, 1, 0, 0, 'active'),
    (151,           5,                      'Milk',              'Dairy',   16,   'fl_oz', 'volume', None, 16,  '2026-02-10', '2026-02-22', 0, 1, 0, 1, 0, 0, 'active'),
    (152,           5,              'Parmesan Cheese',   'Dairy',  200,   'g',     'weight', 200, None, '2026-02-20', '2026-04-20', 0, 1, 0, 1, 0, 0, 'active'),
    (153,           5,              'Mozzarella Cheese', 'Dairy',  250,   'g',     'weight', 250, None, '2026-02-20', '2026-03-10', 0, 1, 0, 1, 0, 0, 'active'),
    (154,           5,              'Ricotta Cheese',    'Dairy',  200,   'g',     'weight', 200, None, '2026-02-20', '2026-03-05', 0, 1, 0, 1, 0, 0, 'active'),
    (155,           5,              'Basil (Fresh)',     'Produce', 30,   'g',     'weight', 30,  None, '2026-02-20', '2026-02-27', 0, 1, 0, 1, 0, 0, 'active'),
    (156,           5,              'Oregano (Dried)',   'Pantry',  20,   'g',     'weight', 20,  None, '2026-02-20', '2028-02-20', 0, 0, 0, 1, 0, 0, 'active'),
    (157,           5,              'Thyme (Dried)',     'Pantry',  20,   'g',     'weight', 20,  None, '2026-02-20', '2028-02-20', 0, 0, 0, 1, 0, 0, 'active'),
    (158,           5,              'Garlic',            'Produce',100,   'g',     'weight', 100, None, '2026-02-20', '2026-03-15', 0, 1, 0, 1, 0, 0, 'active'),
    (159,           5,              'Crushed Tomato',    'Canned',   1,   'can',   'count', None, None, '2026-02-20', '2028-02-20', 0, 1, 0, 1, 0, 0, 'active'),
    (160,           5,              'Tomato Paste',      'Canned',   1,   'can',   'count', None, None, '2026-02-20', '2028-02-20', 0, 1, 0, 1, 0, 0, 'active'),
    (161,           5,             'Pesto Sauce',       'Pantry', 200,   'g',     'weight', 200, None, '2026-02-20', '2027-02-20', 0, 1, 0, 1, 0, 0, 'active'),
    (162,           5,              'Balsamic Vinegar',  'Pantry', 250,   'ml',    'volume', None, 250, '2026-02-20', '2028-02-20', 0, 0, 0, 1, 0, 0, 'active'),
    (163,           5,              'Red Wine Vinegar',  'Pantry', 250,   'ml',    'volume', None, 250, '2026-02-20', '2028-02-20', 0, 0, 0, 1, 0, 0, 'active'),
    (164,           5,                  'Spaghetti',         'Grains', 500,   'g',     'weight', 500, None, '2026-02-20', '2027-02-20', 0, 0, 0, 1, 0, 0, 'active'),
    (165,           5,                  'Fettuccine',        'Grains', 500,   'g',     'weight', 500, None, '2026-02-20', '2027-02-20', 0, 0, 0, 1, 0, 0, 'active'),
    (166,           5,                  'Penne Pasta',       'Grains', 500,   'g',     'weight', 500, None, '2026-02-20', '2027-02-20', 0, 0, 0, 1, 0, 0, 'active'),
    (167,           5,                  'Arborio Rice',      'Grains', 500,   'g',     'weight', 500, None, '2026-02-20', '2027-02-20', 0, 0, 0, 1, 0, 0, 'active'),
    (168,           5,             'Polenta (Cornmeal)','Grains', 500,   'g',     'weight', 500, None, '2026-02-20', '2027-02-20', 0, 0, 0, 1, 0, 0, 'active'),
    (169,           5,               'Red Pepper Flake',  'Pantry',  20,   'g',     'weight', 20,  None, '2026-02-20', '2028-02-20', 0, 0, 0, 1, 0, 0, 'active'),
    (170,           5,              'Italian Bread Crumb','Pantry',300,   'g',     'weight', 300, None, '2026-02-20', '2027-02-20', 0, 0, 0, 1, 0, 0, 'active'),
    (171,           5,              'Sun-Dried Tomato',  'Pantry', 150,   'g',     'weight', 150, None, '2026-02-20', '2027-02-20', 0, 0, 0, 1, 0, 0, 'active'),
    (172,           5,              'Artichoke Heart',   'Canned',   1,   'can',   'count', None, None, '2026-02-20', '2028-02-20', 0, 1, 0, 1, 0, 0, 'active'),
    (173,           5,                  'Mushroom',          'Produce',200,   'g',     'weight', 200, None, '2026-02-20', '2026-02-27', 0, 1, 0, 1, 0, 0, 'active'),
    (174,           5,                  'Zucchini',          'Produce',300,   'g',     'weight', 300, None, '2026-02-20', '2026-03-05', 0, 1, 0, 1, 0, 0, 'active'),
    (175,           5,                  'Eggplant',          'Produce',400,   'g',     'weight', 400, None, '2026-02-20', '2026-03-05', 0, 1, 0, 1, 0, 0, 'active'),
    (176,           5,                  'Cilantro',          'Produce', 30,   'g',     'weight', 30,  None, '2026-02-20', '2026-02-27', 0, 1, 0, 1, 0, 0, 'active'),
    (177,           5,                      'Lime',              'Produce',  4,   'count', 'count', None, None, '2026-02-20', '2026-03-01', 0, 1, 0, 1, 0, 0, 'active'),
    (178,           5,                  'Avocado',           'Produce',  2,   'count', 'count', None, None, '2026-02-20', '2026-02-27', 0, 1, 0, 1, 0, 0, 'active'),
    (179,           5,          'Corn Tortilla Chip','Snack',  300,   'g',     'weight', 300, None, '2026-02-20', '2027-02-20', 0, 0, 0, 1, 0, 0, 'active'),
    (180,           5,          'Ground Beef',          'Meat',          1,      'lb',                'weight',             None,          None,        '2027-02-14', '2027-02-19',        1,          1,      0,                1,                 0,         0,      'active'),
   
]





cursor.executemany("""
INSERT INTO inventory (id,player_id, name, category, quantity, unit, measurement_type, quantity_grams, quantity_ml, purchase_date, best_by, raw_meat, perishable, opened, donation_allowed, decomposition_flag, price, status)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", sample_items)

cursor.executemany("""
INSERT OR IGNORE INTO inventory (id, player_id, name, category, quantity, unit, measurement_type, quantity_grams, quantity_ml, purchase_date, best_by, raw_meat, perishable, opened, donation_allowed, decomposition_flag, price, status)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", sample_items_2)

cursor.executemany("""
INSERT OR IGNORE INTO inventory (id, player_id, name, category, quantity, unit, measurement_type, quantity_grams, quantity_ml, purchase_date, best_by, raw_meat, perishable, opened, donation_allowed, decomposition_flag, price, status)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", sample_items_3)

cursor.executemany("""
INSERT OR IGNORE INTO inventory (id, player_id, name, category, quantity, unit, measurement_type, quantity_grams, quantity_ml, purchase_date, best_by, raw_meat, perishable, opened, donation_allowed, decomposition_flag, price, status)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", sample_items_4)

cursor.executemany("""
INSERT OR IGNORE INTO inventory (id, player_id, name, category, quantity, unit, measurement_type, quantity_grams, quantity_ml, purchase_date, best_by, raw_meat, perishable, opened, donation_allowed, decomposition_flag, price, status)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", sample_items_5)



conn.commit()
conn.close()


