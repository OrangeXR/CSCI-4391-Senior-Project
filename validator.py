import sqlite3
import json
from unit_conversion import normalize_quantity 
from expiry import sort_inventory

class recipe_validator:
    def __init__(self):
        self.DB_PATH = 'src/instance/inventory.db'
        self.PLAYER_ID = 1 # for testing
    
    def get_db(self): 
        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn 
    
    def get_active_inventory(self, player_id): 
        conn = self.get_db()
        cursor = conn.cursor()
        
        cursor.execute(""" 
                       SELECT name, category, quantity, unit, measurement_type,
                       quantity_grams, quantity_ml,
                       best_by, opened
                       FROM inventory
                       WHERE player_id = ? AND status = 'active'
                       """, (player_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
            
    def validate_AI_recipe(self, recipe_json_str, player_id):
        print("\n--- VALIDATOR STARTED ---")
        # fetch current inventory and build a lookup dictionary
        inventory = self.get_active_inventory(player_id)
        # checks expired 
        print("\n--- VALIDATOR INVENTORY CHECK ---")
        expired, about_to_expire, fresh = sort_inventory(inventory)
        
        # Make everything lowercase for easy matching
        exp_lower = [name.lower() for name in expired]
        ate_lower = [name.lower() for name in about_to_expire]
        fresh_lower = [name.lower() for name in fresh]

        for item in inventory:
            name = item['name']
            name_lower = name.lower()
            
            if name_lower in exp_lower:
                status = "EXPIRED"
            elif name_lower in ate_lower:
                status = "ABOUT TO EXPIRE"
            elif name_lower in fresh_lower:
                status = "FRESH"
            else:
                status = "UNKNOWN"
                
            print(f"- {name}: {item['quantity']} {item['unit']} [{status}]")
        print("---------------------------------\n")
        # --- END DEBUGGING BLOCK ---

        inv_dict = {}
        for item in inventory:
            name = item['name'].lower()
            if name not in inv_dict:
                inv_dict[name] = {'grams': 0.0, 'ml': 0.0, 'count': 0.0}
            inv_dict[name]['grams'] += float(item.get('quantity_grams') or 0.0)
            inv_dict[name]['ml'] += float(item.get('quantity_ml') or 0.0)
            
            if item.get('measurement_type') == 'count':
                inv_dict[name]['count'] += float(item.get('quantity') or 0.0)
        # print(f"Active Pantry Dictionary Built: {inv_dict}") // can be removed, debugging statement will print pantry contents

        # parse the LLM's JSON response
        try:
            # print(f"\n Raw AI output received by validator:\n{recipe_json_str}\n")
            # debugging statemtn above, can be removed to see output validator receives
            
            clean_str = recipe_json_str.strip()
            # Strip markdown formatting just in case the AI wraps the JSON in ```json
            if clean_str.startswith('```json'):
                clean_str = clean_str[7:]
            if clean_str.startswith('```'):
                clean_str = clean_str[3:]
            if clean_str.endswith('```'):
                clean_str = clean_str[:-3]
                
            recipe_data = json.loads(clean_str.strip())
            print("JSON successfully parsed.")
            
        except json.JSONDecodeError:
            print("Validator Failed: Could not parse JSON.")
            return False, "Formatting error: Please output strictly in the requested JSON format."

        ingredients_used = recipe_data.get("ingredients_used", [])
        print(f"Ingredients requested by AI: {ingredients_used}")
        
        # validate each ingredient against the 4 rules
        for req in ingredients_used:
            req_name = req.get('name', '').lower()
            req_qty = float(req.get('quantity') or 0.0)
            req_unit = req.get('unit', 'each')
            req_type = req.get('measurement_type', 'count')

            if req_name in exp_lower:
                return False, f"Ingredient '{req_name}' is expired and cannot be used."
            
           # print(f"\n Checking ingredient: {req_name} (Needs {req_qty} {req_unit}, Type: {req_type})") // can be removed for debugging
            # exists in pantry, fuzzy match
            matched_inv = None
            for inv_name in inv_dict.keys():
                if req_name in inv_name or inv_name in req_name:
                    matched_inv = inv_dict[inv_name]
                    print(f"      * Found match in pantry: '{inv_name}'")
                    break
                    
            if not matched_inv:
                print(f"FAILED: '{req_name}' not found in pantry.")
                return False, f"Ingredient '{req_name}' is not in the pantry."
            
            # convert units to grams/ml/count as needed for comparison
            try:
                req_grams, req_ml = normalize_quantity(req_qty, req_unit, req_type)
            except Exception as e:
                print(f" Warning: normalize_quantity threw an error: {e}. Defaulting to 0.0")
                req_grams, req_ml = 0.0, 0.0

            # BUG FIX: Ensure req_grams and req_ml are floats, not None
            req_grams = float(req_grams if req_grams is not None else 0.0)
            req_ml = float(req_ml if req_ml is not None else 0.0)

            print(f"      * Converted AI requirements: {req_grams}g, {req_ml}ml")
            print(f"      * Pantry actually has: {matched_inv['grams']}g, {matched_inv['ml']}ml, {matched_inv['count']} count")

            # check if amount required is available in pantry
            if req_type == 'volume':
                if req_ml > matched_inv['ml']:
                    print(f"FAILED MATH: Need {req_ml}ml, only have {matched_inv['ml']}ml.")
                    return False, f"Not enough '{req_name}'. Need {req_ml}ml, but only have {matched_inv['ml']}ml available. Please scale down portions/servings."
                else:
                    print("Volume check passed!")
                    
            elif req_type == 'weight': 
                if req_grams > matched_inv['grams']:
                    print(f"FAILED MATH: Need {req_grams}g, only have {matched_inv['grams']}g.")
                    return False, f"Not enough '{req_name}'. Need {req_grams}g, but only have {matched_inv['grams']}g available. Please scale down portions/servings."
                else:
                    print("Weight check passed!")
                    
            elif req_type == 'count':
                if req_qty > matched_inv['count']:
                    print(f"FAILED MATH: Need {req_qty}, only have {matched_inv['count']}.")
                    return False, f"Not enough '{req_name}'. Need {req_qty}, but only have {matched_inv['count']} available. Please scale down portions/servings."
                else:
                    print("Count check passed!")
                
        # if pass, then generate recipe
        print("\n--- VALIDATOR PASSED ---")
        return True, recipe_data.get("recipe_text", "Recipe generated successfully.")