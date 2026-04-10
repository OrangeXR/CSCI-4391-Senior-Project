import requests
import os
import sqlite3
import json
from dotenv import load_dotenv
from expiry import sort_inventory
from validator import recipe_validator   #importing everything from validator

class Ai_Chat: 
    # IMPORTANT
    #  I sent the .env file with the api key  in the chat, but I will not be including it in the code repository for security reasons and github gets whiny about it lol
    #  Just drop that .env file in the same directory as this script and it should work fine
    #  I have that .env file added to .gitignore so it wont be included in the repo
    #  thanks guys :3

    def __init__(self):
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
        self.PLAYER_ID = 1 # for testing
        self.MAX_HISTORY = 10 # max number of messages to keep in conversation history to prevent growth
        self.Cook_WORDS = ["recipe", "cook", "cooking", "make", "prepare", "fry",
                           "grill", "roast", "saute", "steam", "boil", "air fry",
                           "meal", "dish", "food idea", "what can i make", "what should i cook",
                           "how to make", "how do i cook", "instructions", "steps",
                           "lunch idea", "dinner idea", "breakfast idea", "snack idea",
                           "meal prep", "quick meal", "easy recipe", "simple recipe"
                           ]
    
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
        if about_to_expire:
            lines.append("\nABOUT TO EXPIRE (Use within 4 days):")
            for item in about_to_expire:
                lines.append(get_item_math(item))
        if fresh:
            lines.append("\nFRESH (Safe for now):")
            for item in fresh:
                lines.append(get_item_math(item))
        if expired:
            lines.append("\nEXPIRED (Recommend compost):")
            for item in expired:
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
            {
                "role": "system",
                "content": (
                    "## ROLE\n"
                    "You are an eco-conscious Food Waste Reducer. Your goal is to create recipes "
                    "using ONLY provided inventory, prioritizing items marked [ABOUT TO EXPIRE].\n\n"
                    
                    "## CONSTRAINTS\n"
                    "- ONLY use provided inventory. Respect available quantities.\n"
                    "- FORBIDDEN: Do not use expired food. Do not provide food safety advice.\n"
                    "- If asked about food safety, respond: 'Sorry, I don't have that info.'\n"
                    "- PRIORITIZE: Use 2-3 [ABOUT TO EXPIRE] items in every recipe to reduce waste.\n\n"
                    
                    "## MEASUREMENT LOGIC\n"
                    "You must match units EXACTLY as provided in the inventory list:\n"
                    "1. WEIGHT (g, lbs): Do NOT convert to volume. Use the exact weight unit.\n"
                    "2. COUNT: Use 'count' only (e.g., '1 count' of onion, not '100g').\n"
                    "3. VOLUME (ml): You may use ml, cups, or tbsp.\n\n"
                    
                    "## OUTPUT FORMAT\n"
                    "1. CHAT: If the user is just greeting or chatting, respond with friendly, concise text.\n"
                    "2. RECIPE: If the user asks for a recipe or cooking advice, you MUST output "
                    "STRICTLY a JSON object. No conversational filler before or after the JSON.\n\n"
                    
                    "### JSON SCHEMA\n"
                    "{\n"
                    '  "recipe_text": "Detailed cooking instructions and tips.",\n'
                    '  "ingredients_used": [\n'
                    '    {"name": "string", "quantity": number, "unit": "string", "measurement_type": "string"}\n'
                    '  ]\n'
                    "}"
                )
            }
        ]
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
                
                #Check if user wants recipe
                user_lower = user_input.lower()
                
                if any(word in user_lower for word in self.Cook_WORDS):
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
                            
                else:
                    print(f"\nLLM: {raw_response}\n")
                    messages.append({"role": "assistant", "content": raw_response})
                    break
            
if __name__ == "__main__":
    Ai_bot = Ai_Chat()
    Ai_bot.chatConsole() 
