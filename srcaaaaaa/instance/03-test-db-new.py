# connects to inventory.db and prints the values of the database, 
# just to make sure everything is working as it should

#import sqlite3 

#conn = sqlite3.connect("inventory.db")
#cursor = conn.cursor()

#cursor.execute("SELECT * FROM inventory")
#for row in cursor.fetchall():
#    print(row)
    
#conn.close()


import sqlite3

conn = sqlite3.connect("src/instance/inventory.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

