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
        "INSERT INTO inventory (name, category, quantity, best_by) VALUES (?,?,?,?)",
        (data["name"], data["category"], data["quantity"], data["best_by"])
    )
    db.commit()
    db.close()