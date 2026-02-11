conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM inventory")
for row in cursor.fechall():
    print(row)
    
conn.close()
