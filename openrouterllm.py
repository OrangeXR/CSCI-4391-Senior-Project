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
        # donation words
        self.Donate_WORDS = ["donate", "donation", "give away", "food bank", "charity", 
                             "share food", "who i can give", "where to donate", 
                             "can i donate", "food pantry", "shelter", "community fridge" 
                            ] 
        # decomposition words 
        self.Decomp_WORDS= ["compost", "decompost", "decomposition", "break down", "breakdown", 
                            "dispose", "disposal", "rot", "organic waste", "throw away", 
                            "get rid of", "expired food", "what i do with expired", 
                            "how to dispose", "bin"
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
                       best_by, opened, perishable, donation_allowed, decomposition_flag, raw_meat
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

                     # include flags 
                    perishable = db_item.get("perishable", 0)
                    don_allowed = db_item.get("donation_allowed", 0)
                    decomp_flag= db_item.get("decomposition_flag", 0)
                    raw_meat = db_item.get("raw_meat", 0)
                    opened = db_item.get("opened", 0)
                    flags=[]
                    if perishable: flags.append("perishable")
                    if don_allowed: flags.append("donation_allowed")
                    if decomp_flag: flags.append("compostable")
                    if raw_meat: flags.append("raw_meat")
                    if opened: flags.append("opened")
                    flag_str= f" [{','.join(flags)}]" if flags else ""
                    return f"- {item_name}: {qty} {unit} (measurement_type: {m_type}{flag_str})"
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
                    "- PRIORITIZE: Use 2-3 [ABOUT TO EXPIRE] items in every recipe to reduce waste.\n"
                    "- Quantities MUST be realistic for cooking.\n"
                    "- Typical cooking amounts: Salt: pinch–5g | Oil: 15–45ml | Spices: under 5g.\n\n"
                    "- NEVER invent ingredients not explicitly listed in the inventory. If an item is not in the inventory, do not use it.\n"
                    
                    "## MEASUREMENT LOGIC\n"
                    "You must match units EXACTLY as provided in the inventory list:\n"
                    "1. WEIGHT (g, lbs): Do NOT convert to volume. Use the exact weight unit.\n"
                    "2. COUNT: Use 'count' only (e.g., '1 count' of onion, not '100g').\n"
                    "3. VOLUME (ml): You may use ml, cups, or tbsp.\n\n"
                    
                     "## OUTPUT FORMAT — FOUR MODES\n\n"
 
                    "### MODE 1: CHAT\n"
                    "For greetings or general questions: respond with friendly, concise plain text.\n\n"
 
                    "### MODE 2: RECIPE\n"
                    "If the user asks for a recipe or cooking advice, return ONLY valid JSON. "
                    "No text before or after. No markdown.\n"
                    "{\n"
                    '  "response_type": "recipe",\n'
                    '  "recipe_title": "string",\n'
                    '  "recipe_text": "string (step-by-step instructions)",\n'
                    '  "ingredients_used": [\n'
                    '    {"name": "string", "quantity": number, "unit": "string", "measurement_type": "string"}\n'
                    '  ]\n'
                    "}\n\n"
 
                    "### MODE 3: DECOMPOSITION\n"
                    "If the user asks about composting, disposing, or decomposing food, "
                    "return ONLY valid JSON listing items flagged as compostable or expired. "
                    "If an item is not EXPIRED or compostable, DO NOT include it in suggestions at all."
                    "Never output placeholder text like 'See notes'."
                    "No text before or after. No markdown.\n"
                    "{\n"
                    '  "response_type": "decomposition",\n'
                    '  "suggestions": [\n'
                    '    {\n'
                    '      "name": "string",\n'
                    '      "method": "string (e.g. home compost, green bin, bokashi, worm bin)",\n'
                    '      "notes": "string — a specific tip for THIS item. Examples: '
                    '       avocado pit: remove hard pit before composting | '
                    '       citrus: use sparingly in worm bins, high acidity | '
                    '       raw meat: bokashi only, never open compost | '
                    '       cooked food: green bin only | '
                    '       eggplant: chop skin into small pieces, flesh breaks down fast | '
                    '       banana peel: great nitrogen source, compost whole | '
                    '       bread: attracts pests, use bokashi or bury deep. '
                    '       Give a UNIQUE note per item — never repeat the same note."\n'
                    '    }\n'
                    '  ]\n'
                    "}\n\n"
 
                    "### MODE 4: DONATION\n"
                    "If the user asks about donating food, return ONLY valid JSON listing items "
                    "ONLY valid JSON listing items marked donation_allowed=1."
                    "DO NOT include any items unless explicitly marked donation_allowed=1."
                    "If unsure, exclude the item.\n"
                    "{\n"
                    '  "response_type": "donation",\n'
                    '  "suggestions": [\n'
                    '    {\n'
                    '      "name": "string — item name exactly as in inventory",\n'
                    '      "quantity": number - REQUIRED, use the quantity from inventory,\n'
                    '      "unit": "string — REQUIRED, use the unit from inventory",\n'
                    '      "donation_tip": "string — REQUIRED, specific tip e.g. bring to food bank sealed, check best-by before drop-off, community fridge accepted"\n'
                    '    }\n'
                    '  ]\n'
                    "}\n"
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

            user_lower = user_input.lower()

            # ==============
            # recipe section
            # ===============
            if any(word in user_lower for word in self.Cook_WORDS):
                MAX_RETRIES = 1
                for attempt in range(MAX_RETRIES + 1):
                    raw_response = self.getLLMResponse(messages)
                    try:
                        parsed = json.loads(raw_response)  # validate JSON structure only
                        if "ingredients_used" not in parsed:
                            raise json.JSONDecodeError("Missing ingredients_used", raw_response, 0)
                    except json.JSONDecodeError:
                        print("\nSystem: LLM returned invalid JSON. Regenerating...\n")
                        messages.append({"role": "assistant", "content": raw_response})
                        messages.append({
                            "role": "user",
                            "content": (
                                "Return ONLY valid JSON. Your previous response was not valid JSON. "
                                "Please fix it and follow the required JSON schema exactly. "
                                "Do NOT include any explanation, just return the JSON."
                            )
                        })
                        continue
                    
                    #send recie to validator
                    is_valid, validation_msg = call_validator.validate_AI_recipe(raw_response, self.PLAYER_ID)
 
                    if is_valid:
                        #print recipe
                        parsed = json.loads(raw_response)
                        print("\n--- VALID RECIPE ---\n")
                        print(parsed.get('recipe_title', 'Recipe'))
                        print("\nIngredients:")
                        for ing in parsed["ingredients_used"]:
                            print(f"- {ing['name']}: {ing['quantity']} {ing['unit']}")
                        print(parsed["recipe_text"])
                        break
                    else:
                        #if fail
                        if attempt < MAX_RETRIES:
                            print(f"\n[System: Recipe failed validation: {validation_msg}. Asking AI to regenerate...]\n")
                            messages.append({"role": "assistant", "content": raw_response})
                            messages.append({
                                "role": "user",
                                "content": (
                                    f"Your previous response failed validation because: {validation_msg}.\n"
                                    "Return ONLY valid JSON.\n"
                                    "Do NOT include any explanation.\n"
                                    "Fix ingredient quantities to match the inventory.\n"
                                    "Follow the required JSON schema exactly."
                                )
                            })
                        else:
                            print(f"\nLLM: I tried to make a recipe, but we don't have enough ingredients. {validation_msg}\n")
                            messages.append({"role": "assistant", "content": f"Failed: {validation_msg}"})
            # ================
            # Donation section
            # ================
            elif any(word in user_lower for word in self.Donate_WORDS):
                MAX_RETRIES = 1
                for attempt in range(MAX_RETRIES + 1):
                    raw_response = self.getLLMResponse(messages)
                    try:
                        parsed = json.loads(raw_response)
                        if "suggestions" not in parsed: raise ValueError()
                        print("\n--- DONATION SUGGESTIONS ---\n")
                        for s in parsed.get("suggestions", []):
                            qty = s.get("quantity", "")
                            unit = s.get("unit", "")
                            qty_str = f": {qty} {unit}".strip(": ") if qty else ""
                            print(f"- {s.get('name', 'Item')}{qty_str}")
                            print(f"  Tip: {s.get('donation_tip', 'Check with local food bank')}")
                        messages.append({"role": "assistant", "content": raw_response})
                        break
                    except (json.JSONDecodeError, ValueError):
                    
                        if attempt < MAX_RETRIES:
                            print("\nSystem: LLM returned invalid JSON. Regenerating...\n")
                            messages.append({"role": "assistant", "content": raw_response})
                            messages.append({
                                "role": "user",
                                "content": (
                                    "Return ONLY valid JSON with response_type 'donation' "
                                    "and a 'suggestions' list. No explanation. Follow the schema exactly."
                                )
                            })
                        else:
                            print(f"\nLLM: {raw_response}\n")
                            messages.append({"role": "assistant", "content": raw_response})
            
            # =====================     
            # Decomposition section
            # =====================
            elif any(word in user_lower for word in self.Decomp_WORDS):
                MAX_RETRIES = 1
                for attempt in range(MAX_RETRIES + 1):
                    raw_response = self.getLLMResponse(messages)
                    try:
                        parsed = json.loads(raw_response)
                        if "suggestions" not in parsed: raise ValueError()
                        print("\n--- DECOMPOSITION SUGGESTIONS ---\n")
                        for s in parsed.get("suggestions", []):
                            method = s.get("method") or "Compost"
                            print(f"- {s.get('name', 'Item')}: {method}")
                            print(f"  Note: {s.get('notes', 'Standard organic disposal')}")
                        messages.append({"role": "assistant", "content": raw_response})
                        break
                    except (json.JSONDecodeError, ValueError):
                        if attempt < MAX_RETRIES:
                            print("\nSystem: LLM returned invalid JSON. Regenerating...\n")
                            messages.append({"role": "assistant", "content": raw_response})
                            messages.append({
                                "role": "user",
                                "content": (
                                    "Return ONLY valid JSON with response_type 'decomposition' "
                                    "and a 'suggestions' list. No explanation. Follow the schema exactly."
                                )
                            })
                        else:
                            print(f"\nLLM: {raw_response}\n")
                            messages.append({"role": "assistant", "content": raw_response})
            # ============
            # general chat
            # ============
            else:
               raw_response = self.getLLMResponse(messages)
               print(f"\nLLM: {raw_response}\n")
               messages.append({"role": "assistant", "content": raw_response})
if __name__ == "__main__":
    Ai_bot = Ai_Chat()
    Ai_bot.chatConsole() 
