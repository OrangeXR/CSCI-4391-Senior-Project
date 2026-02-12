# connects to inventory.db and prints the values of the database, 
# just to make sure everything is working as it should

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM inventory")
for row in cursor.fechall():
    print(row)
    
conn.close()
