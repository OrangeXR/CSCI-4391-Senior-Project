import sqlite3

# connects to inventory.db and prints the values of the database, 
# just to make sure everything is working as it should

#import sqlite3 

#conn = sqlite3.connect("inventory.db")
#cursor = conn.cursor()

#cursor.execute("SELECT * FROM inventory")
#for row in cursor.fetchall():
#    print(row)
    
#conn.close()


conn = sqlite3.connect("src/instance/inventory.db")
cursor = conn.cursor()

## Print Tables in DB
#cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
#print(cursor.fetchall())

## Raw invetory
#cursor.execute("SELECT * FROM inventory")
#print(cursor.fetchall())
print("========== Players ==========")
cursor.execute("SELECT * FROM players")
rows = cursor.fetchall()
for row in rows:
    print(row)

print("========== Inventory ==========")
## one row per line
cursor.execute("SELECT * FROM inventory")
rows = cursor.fetchall()
for row in rows:
    print(row)


conn.close()

