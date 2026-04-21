import sqlite3

def get_db():
    conn = sqlite3.connect("src/instance/inventory.db")
    conn.row_factory = sqlite3.Row
    return conn