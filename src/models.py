''' ======================
    connect to database.py 
    to connect to db
    ====================== '''
from database import get_db 

''' =====================
    Connects to db to 
    retrieve every row
    and closes connection
    ===================== '''
def get_all_items():
    db = get_db()
    items = db.execute("SELECT * FROM inventory").fetchall()
    db.close()
    return [dict(row) for row in items]

''' ======================= 
    Connects to db, 
    inserts item and
    closes connection to db 
    ======================= '''
def add_item(data):
    db = get_db()
    db.execute(
        "INSERT INTO inventory (name, category, quantity, unit, measurement_type, quantity_grams, quantity_ml, purchase_date, best_by, raw_meat, perishable, opened, donation_allowed, decomposition_flag, price ,status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (data["name"], data["category"], data["quantity"], data["unit"], data["measurement_type"], data["quantity_grams"], data["quantity_ml"], data["purchase_date"], data["best_by"], data["raw_meat"], data["perishable"], data["opened"], data["donation_allowed"], data["decomposition_flag"], data["price"], data["status"])
    )
    db.commit()
    db.close()