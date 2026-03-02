import sqlite3


class recipe_validator:
    def __init__(self):
        # db path + other variables
        self.DB_PATH = 'src/instance/inventory.db'
        self.PLAYER_ID = 1 # for testing
    
    def get_db(self): # function to connect to the database
        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn 
    
    def get_active_inventory(self,player_id): # function to get active inventory items for a player from the database
        conn = self.get_db()
        cursor = conn.cursor()
        
        cursor.execute(""" 
                       SELECT name, category, quantity, unit,
                       quantity_grams, quantity_ml,
                       best_by, opened
                       FROM inventory
                       WHERE player_id = ? AND status = 'active'
                       """, (player_id,)) # fetch all active inventory items for the player, including quantity in grams and ml for better precision in recipe suggestions
        rows = cursor.fetchall()
        conn.close()
        print (dict(row) for row in rows)
        return [dict(row) for row in rows] # return list of dicts representing inventory items, each dict has keys: name, category, quantity, unit, quantity_grams, quantity_ml, best_by, opened
    
    def validate_AI_recipe(self,recipe,player_id):
        return("Still thinking lol")
    
    
if __name__ == "__main__":
    call=recipe_validator()
    Justcheking=call.get_active_inventory(call.PLAYER_ID)
    print(Justcheking)
