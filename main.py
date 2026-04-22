import requests
import os
import sqlite3
import json
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from expiry import sort_inventory
from validator import recipe_validator   #importing everything from validator

# ==================
# open db connection
# ==================
def get_db():
    conn = sqlite3.connect("src/instance/inventory.db")
    conn.row_factory = sqlite3.Row
    return conn




# ==================
# choose user
# ==================
def choose_player():
    db = get_db() 
    players = db.execute("SELECT id, name FROM players").fetchall()
    db.close()
    
    print("\nAvailable Players:")
    for p in players: 
        print(f"{p['id']}: {p['name']}") 
  
    player_id = int(input("\nEnter player ID: "))

    # Fetch stored password hash
    stored_hash = get_player_password_hash(player_id)
   
    if stored_hash is None:
        print("Invalid player ID.")   
        return choose_player()
      
    # Ask for password until correct 
    while True:
        password = input("Enter password: ").strip() 
    
        if check_password_hash(stored_hash, password):
            print("Login successful!\n") 
            return player_id
        else:    
            print("Incorrect password. Try again.\n")


# ======================================                         
# Validate Login(get hash from database)                         
# ======================================                           
def get_player_password_hash(player_id):
    db = get_db()
    row = db.execute(
        "SELECT password_hash FROM players WHERE id = ?",
        (player_id,)
    ).fetchone()
    db.close()
    return row["password_hash"] if row else None





# =====================
# get inventory
# =====================
def get_inventory(player_id):
    db = get_db()
    items = db.execute(
        "SELECT * FROM inventory WHERE player_id = ? AND status = 'active'",
        (player_id,)
    ).fetchall()
    db.close()
#    return (items) # no longer needed with table being printed in function

    items = sorted(items, key=lambda item: item["name"].lower())

    print("\n========================= Inventory =========================")

    # Labels for inventory table columns
    print(f"{'Name'.ljust(30)} {'Quantity'.ljust(8)} {'Unit'.ljust(10)} {'Best By'}")
    print("-" * 61)

    for item in items:
        print(
            f"{item['name'].ljust(30)} "
            f"{str(item['quantity']).ljust(8)} "
            f"{item['unit'].ljust(10)} "
            f"{item['best_by']}"
        )
# =====================
# get items by date
# =====================
def get_inventory_by_date(player_id):
    db = get_db()
    items = db.execute(
        """
        SELECT name, quantity, unit, best_by
        FROM inventory
        WHERE player_id = ? AND status = 'active'
        ORDER BY best_by ASC
        """,
        (player_id,)
    ).fetchall()
    db.close()

    print("\n================= Inventory by Best-By Dates ================")
    if not items:
        print("No active inventory items found.")
        return
    
    # Labels for inventory table columns
    print(f"{'Name'.ljust(30)} {'Quantity'.ljust(8)} {'Unit'.ljust(10)} {'Best By'}")
    print("-" * 61)


    for item in items:
        name = item["name"]
        quantity = str(item["quantity"])
        unit = item["unit"]
        best_by = item["best_by"] if item["best_by"] else "No date"

        # Table printout with db values
        print(
            f"{name.ljust(30)} " f"{quantity.rjust(8)} " f"{unit.ljust(10)} " f"{best_by}" 
        )



# ================================================================================================================================
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv  Original Chat with AI
# ================================================================================================================================
class Ai_Chat: 
    # IMPORTANT
    #  I sent the .env file with the api key  in the chat, but I will not be including it in the code repository for security reasons and github gets whiny about it lol
    #  Just drop that .env file in the same directory as this script and it should work fine
    #  I have that .env file added to .gitignore so it wont be included in the repo
    #  thanks guys :3

    def __init__(self, player_id):
        self.PLAYER_ID = player_id
        load_dotenv()
        # load environment variables from .env file
        # # set api key and endpoint 
        self.API_KEY = os.getenv("OPENROUTER_API_KEY")
        if not self.API_KEY:
            raise ValueError("API key not found. Please check your .env file and ensure OPENROUTER_API_KEY is set.")
        self.API_URL = 'https://openrouter.ai/api/v1/chat/completions' # api url, program will send requests and get responses from here
        # restricted words/topics, chatbot will not responsd
        self.RESTRICTED_WORDS = ["poop"]
        # db path + other variables
        self.DB_PATH = 'src/instance/inventory.db'
        self.PLAYER_ID = player_id #1 # for testing
        self.MAX_HISTORY = 10 # max number of messages to keep in conversation history to prevent growth
    
    # DB setup
    def get_db(self): # function to connect to the database
        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn 
    
    def get_active_inventory(self,player_id): # function to get active inventory items for a player from the database
        conn = self.get_db()
        cursor = conn.cursor()
        
        cursor.execute(""" 
                       SELECT name, category, quantity, unit, measurement_type,
                       quantity_grams, quantity_ml,
                       best_by, opened
                       FROM inventory
                       WHERE player_id = ? AND status = 'active'
                       """, (player_id,)) # fetch all active inventory items for the player, including quantity in grams and ml for better precision in recipe suggestions
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows] # return list of dicts representing inventory items, each dict has keys: name, category, quantity, unit, quantity_grams, quantity_ml, best_by, opened
    
    
    def build_inventory_context(self,items):
        if not items:
            return "No food items in inventory."
        # get sorted lists
        expired, about_to_expire, fresh = sort_inventory(self.PLAYER_ID)
        # start the context
        lines = ["Here is my current inventory:"]

        # Helper function to grab the math from the database 
        def get_item_math(item_name):
            for db_item in items:
                if db_item.get('name', '').lower() == item_name.lower():
                    qty = db_item.get('quantity', 0)
                    unit = db_item.get('unit', 'each')
                    m_type = db_item.get('measurement_type', 'count')
                    return f"- {item_name}: {qty} {unit} (measurement_type: {m_type})"
            return f"- {item_name}" # Fallback if not found

        # add each category
        if expired:
            lines.append("\nEXPIRED (Recommend compost):")
            for item in expired:
                lines.append(get_item_math(item))
        if about_to_expire:
            lines.append("\nABOUT TO EXPIRE (Use within 4 days):")
            for item in about_to_expire:
                lines.append(get_item_math(item))
        if fresh:
            lines.append("\nFRESH (Safe for now):")
            for item in fresh:
                lines.append(get_item_math(item))
        
        return "\n".join(lines)

        # Citations:
        # ---------
        # Implemented using a Google Gemini prompt as a guideline:
        # "and do return like: expired, about_to_expire, fresh"


        #Inspired From https://coderivers.org/blog/json-save-python/
        #Still Needs improvment
   # def save_result_JSON(self, save_recipe_Json, file="saved_recipe.json"):
        '''try:
            with open(file, "w") as recipe_file:
                json.dump(save_recipe_Json, recipe_file)
        except (IOError, TypeError) as e:
            print(f"Error occurred: {e}")'''
            
# get llm response functions
    def getLLMResponse(self,messages):
        # set headers and data for the request
        headers = {
            "Authorization": f"Bearer {self.API_KEY}",
            "Content-Type": "application/json"
            }
        
        data = {
            "model": "arcee-ai/trinity-large-preview:free",  # using trinity large preview free model
            "messages": messages # will declare limits at start of chat loop
            }
        try:
            response = requests.post(self.API_URL, headers=headers, json=data)
            response.raise_for_status() # check for errors
            responseData = response.json()
            
            return responseData['choices'][0]['message']['content'] # return the content of the response
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as e:
            return f"Error: {e}"
    
# console chat loop

    def chatConsole(self):
        print("Welcome! The model is Trinity Large Preview (free). Type 'quit' to exit.\n")
        # this is where the chatbot will be constrained
        messages = [
            { "role": "system", 
             "content": (
                 "You are a helpful, eco-conscious Food waste reducer\n"
                 "Only use the inventory provided to you.\n"
                 "When suggesting recipes or meals:\n"
                 "- Be specific and precise with ingredient quantities.\n"
                 "- Use realistic measurements (grams, ml, tbsp, cups, etc.).\n"
                 "- Respect the available inventory amounts.\n"
                 "- Do not suggest quantities that exceed what is available.\n"
                 "- If quantity data is missing, state assumptions clearly.\n"
                 "Keep responses concise but practical and clear.\n"
                 "Do not give food safety recommendations at all. Anything involving food safety, respond 'Sorry, I don't have that info.'\n"
                "CRITICAL RULES:\n"
                 "1. You MUST output your response STRICTLY as a JSON object. No conversational text outside the JSON.\n"
                 "2. DO NOT USED EXPIRED FOOD: You are forbidden from using expired food in recipes.\n"
                 "3. MATCH UNITS EXACTLY: You must use the exact `measurement_type` and `unit` provided in the inventory list.\n"
                 "   - If an item is listed in 'g' or 'lbs' (weight), you CANNOT use cups, tbsp, or volume measurements. You MUST request it in grams or lbs.\n"
                 "   - If an item is listed as 'count', you MUST use 'count' (e.g., do not ask for 15 oz of canned beans if it says 1 count).\n"
                 "   - If an item is listed in 'ml' (volume), use ml, cups, or tbsp.\n"
                 "4. Use this exact format:\n"
                 "{\n"
                 '  "recipe_text": "Your natural conversational text, recipe steps, and tips go here...",\n'
                 '  "ingredients_used": [\n'
                 '    {"name": "rice", "quantity": 200, "unit": "g", "measurement_type": "weight"}\n'
                 "  ]\n"
                 "}\n"
             )
            }]
        call_validator = recipe_validator()

        while True:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit"]:
                print("Goodbye!")
                break
            #  check for forbidden words/topics
            if any(word in user_input.lower() for word in self.RESTRICTED_WORDS):
                print("LLM: Sorry, I can't discuss that topic.\n")
                continue

            # pull latest db items every turn 
            inventory_items = self.get_active_inventory(self.PLAYER_ID)
            inventory_context = self.build_inventory_context(inventory_items)
            # append user message to conversation
            messages.append({"role": "system",
                             "content": f"Current Inventory:\n{inventory_context}" # provide current inventory context to the LLM every turn so it can make informed suggestions based on what the player has available
                             })

            messages.append({"role": "user", "content": user_input}) 
        
             # limit conversation history to last 10 messages to stay within token limits
            messages[:] = messages[-self.MAX_HISTORY:]

            MAX_RETRIES = 1 # retries for recipe generation if validation fails, can adjust as needed
            for attempt in range(MAX_RETRIES + 1):
                raw_response = self.getLLMResponse(messages) 
                
                # send recipe to validator
                is_valid, validation_msg = call_validator.validate_AI_recipe(raw_response, self.PLAYER_ID)
                
                if is_valid:
                    # pass, output recipe to user
                    print(f"\nLLM: {validation_msg}\n") 
                    
                    # save context so the llm remembers what it just said
                    messages.append({"role": "assistant", "content": validation_msg})
                    
                    break # break out of the retry loop
                    
                else:
                    # if fail:
                    if attempt < MAX_RETRIES:
                        print(f"\n[System: Recipe failed validation: {validation_msg}. Asking AI to regenerate and scale down...]\n")
                        # add the failure to the context and loop again to regenerate
                        messages.append({"role": "assistant", "content": raw_response})
                        messages.append({"role": "user", "content": f"Your previous recipe failed validation because: {validation_msg}. Please rewrite the recipe to fix this (e.g., reduce servings or omit the ingredient) and output valid JSON again."})
                    else:
                        print(f"\nLLM: I tried to make a recipe, but we don't have enough ingredients. {validation_msg}\n")
                        messages.append({"role": "assistant", "content": f"Failed: {validation_msg}"})
 

# ================================================================================================================================
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  Original Chat with AI
# ================================================================================================================================



# =====================================================================================================
# =====================================================================================  Select Options
# =====================================================================================================
def main():
    # ===========
    # Select User
    # ===========
    print("\n=== Binny & Bloom ===")
    player_id = choose_player()

    # =========
    # Main Menu
    # =========
    while True:
        print("\nOptions:")
        print("1. View Inventory")
        print("2. View Foods + Best-By Dates")
#        print("3. Add Item to Inventory") # (a bit annoying in terminal)
        print("3. Generate Binny Menu")
        print("4. Logout")
        print("5. Exit")
        choice = input("\nChoose an option: ")
# =====================================================================================  1. Get User Inventory
        if choice == "1":
            get_inventory(player_id)
# =====================================================================================  2. Get/sort inventory by date   
        elif choice == "2":
            get_inventory_by_date(player_id)
# =====================================================================================  3. Add an item to user inventory (not sure if we'll use it in terminal)           
#        elif choice == "3":
#            add_item(player_id)
# =====================================================================================  3. Recipe generator
        elif choice == "3":
                Ai_bot = Ai_Chat(player_id)
                Ai_bot.chatConsole() 
                #binny_menu(player_id)
# =====================================================================================  4. Logout
        elif choice == "4":
                print("\nLogging out...\n")
                return  "logout"# <-- sends user back to player select
# =====================================================================================  5. Exit
        elif choice == "5":
            print("Goodbye!")
            return "exit"

        else:
            print("Invalid choice.")



if __name__ == "__main__":
    while True:  
        result = main() # <--- Loop

        if result == "logout": 
            continue    # <--- Change user
        if result == "exit":
            break       # <---- Exit
