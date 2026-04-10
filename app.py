from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
import requests
import sqlite3
from datetime import datetime, timedelta
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from unit_conversion import normalize_quantity
from expiry import get_expiry_date

# ========================
# Create Flask application
# ========================
app = Flask(__name__)
app.secret_key = "super-secret-key"

BASE_DIR = app.root_path
load_dotenv()  # Load .env file



UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "profile_pics")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# =============
# Connect to db
# =============
def get_db():
    conn = sqlite3.connect("src/instance/inventory.db")
    conn.row_factory = sqlite3.Row
    return conn

# =======================
# define flag calculation
# =======================
from datetime import datetime

def calculate_flags(item):
    category = item["category"].lower().strip()
    name = item["name"].lower()
    opened = int(item.get("opened", 0))

    best_by = datetime.strptime(item["best_by"], "%Y-%m-%d").date()
    today = datetime.today().date()

    # raw meat categories
    raw_meat_category = ["meat", "seafood"]

    # perishable categories (fast spoil)
    perishable_fast = ["meat", "seafood", "dairy", "produce", "prepared"]

    # non-perishable categories (slow spoil)
    non_perishable = ["grains", "pantry", "snacks", "beverages"]

    # raw meat
    raw_meat = 1 if category in raw_meat_category or any(x in name for x in ["chicken", "beef", "pork", "turkey", "fish", "shrimp"]) else 0

    # perishable
    perishable = 1 if category in perishable_fast else 0

    # decomposition
    decomposition_flag = 1 if perishable and best_by < today else 0

    # donation rules
    donation_allowed = 0 if opened == 1 or raw_meat == 1 or decomposition_flag == 1 else 1

    return raw_meat, perishable, donation_allowed, decomposition_flag

# ======================
# Login Required Wrapper
# ======================
def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "player_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper

# =========
# Home Page
# =========
@app.route("/", methods=["GET"])
@login_required
def home_page():
    db = get_db()
    current_player = db.execute(
        "SELECT * FROM players WHERE id = ?", (session["player_id"],)
    ).fetchone()
    db.close()

    return render_template(
        "HomePage.html",
        current_player=current_player
    )

# =========
# Dashboard
# =========
@app.route("/dashboard")
def dashboard():
    # show warning on homepage for foods about to expire in 3 days
    player = session.get('player_id')
    expiring_soon = get_expiry_date(player)

# =============================================================================================================
# Get a list of saved recipes for the user
# =============================================================================================================
    db = get_db()
    meals = db.execute(
        "SELECT id, name, created_at FROM meals WHERE player_id = ? ORDER BY created_at DESC",
        (player,)
    ).fetchall()
    db.close()
# =============================================================================================================
# =============================================================================================================

    if not player:
        # if they aren't logged in, send them to the login page
        return redirect('/login')

    if expiring_soon:
        item_list = ", ".join(expiring_soon)
        flash(f"⚠️ Heads up! Your {item_list} will expire in 3 days.", "warning")

    return render_template('dashboard.html', player=player, meals=meals)

# =====================
# User Profile
# =====================
@app.route("/userprofile", methods=["GET", "POST"])
@login_required
def userprofile():
    player_id = session["player_id"]
    db = get_db()

# ========================================================================= Change profile pic upload
    if request.method == "POST":
        file = request.files.get("profile_picture")

        food_allergies = request.form.get("food_allergies")
        dietary_needs = request.form.get("dietary_needs")
        
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            file.save(filepath)

            db.execute(
                "UPDATE players SET profile_picture = ? WHERE id = ?",
                (filename, player_id)
            )

            db.execute(
                "UPDATE players SET food_allergies = ?, dietary_needs = ? WHERE id = ?",
                (food_allergies, dietary_needs, player_id)
             )
        db.commit()
        db.close()
        return redirect(url_for("userprofile"))

# =========================================================================

    player = db.execute("SELECT * FROM players WHERE id = ?", (player_id,)).fetchone()
   
    db.close()

    return render_template("UserProfile.html", player=player)







# ============================
# Registration Page + Handler
# ============================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        file = request.files["profile_picture"]

        password_hash = generate_password_hash(password)

        filename = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        db = get_db()
        db.execute("""
            INSERT INTO players (name, username, password_hash, profile_picture)
            VALUES (?, ?, ?, ?)
        """, (name, username, password_hash, filename))
        db.commit()
        db.close()

        return redirect("/login")

    return render_template("RegisterPage.html")

# =====================
# Login Page + Handler
# =====================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        player = db.execute(
            "SELECT * FROM players WHERE username = ?", (username,)
        ).fetchone()
        db.close()

        if player and check_password_hash(player["password_hash"], password):
            session["player_id"] = player["id"]
            return redirect("/")

    return render_template("LoginPage.html")

# =======
# Logout
# =======
@app.route("/logout")
def logout():
    session.pop("player_id", None)
    return redirect("/login")



#==========================================
# Inventory Page (uses logged-in player)
#==========================================
@app.route("/inventory",methods=["GET", "POST"])
@login_required
def inventory_page():
    from openrouterllm import Ai_Chat   #importing everything from openrouterllm
    from validator import recipe_validator #importing everything from openrouterllm
    player_id = session["player_id"]

    db = get_db()
    current_player = db.execute(
        "SELECT * FROM players WHERE id = ?", (player_id,)
    ).fetchone()

    items = db.execute(
        "SELECT * FROM inventory WHERE player_id = ? ORDER BY best_by ASC",
        (player_id,)
    ).fetchall()



    

# =====================
# Ai integration 
# =====================
    Response = None    #So errors dont occur 
    
    if request.method == 'POST': #Checking if anything is inputed 
        message = request.form.get("message" ,"hello")  #defualt message 
        
        Chat_box_In = Ai_Chat() #creating an instance
        Chat_validator = recipe_validator()
        inventory_items = Chat_box_In.get_active_inventory(player_id) #getting context for the AI
        inventory_context = Chat_box_In.build_inventory_context(inventory_items)
        
        
        #Message for the AI same as openrouterllm
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
        # append user message to conversation
        messages.append({"role": "system",
                         "content": f"Current Inventory:\n{inventory_context}" # provide current inventory context to the LLM every turn so it can make informed suggestions based on what the player has available
                         })

        messages.append({"role": "user", "content": message}) 
        #getting the response
        MAX_RETRIES = 1 # retries for recipe generation if validation fails, can adjust as needed
        for attempt in range(MAX_RETRIES + 1):
            raw_response = Chat_box_In.getLLMResponse(messages) 
            #Check if user wants recipe
            user_lower = message.lower()
            if any(word in user_lower for word in Chat_box_In.Cook_WORDS):
                # send recipe to validator
                is_valid, validation_msg = Chat_validator.validate_AI_recipe(raw_response, player_id)
                
                if is_valid:
                    # pass, output recipe to user
                    Response=f"\nLLM: {validation_msg}\n"
                    # save context so the llm remembers what it just said
                    messages.append({"role": "assistant", "content": validation_msg})
                    break # break out of the retry loop
                else:
                    # if fail:
                    if attempt < MAX_RETRIES:
                        Response=f"\n[System: Recipe failed validation: {validation_msg}. Asking AI to regenerate and scale down...]\n"
                        # add the failure to the context and loop again to regenerate
                        messages.append({"role": "assistant", "content": raw_response})
                        messages.append({"role": "user", "content": f"Your previous recipe failed validation because: {validation_msg}. Please rewrite the recipe to fix this (e.g., reduce servings or omit the ingredient) and output valid JSON again."})
                    else:
                        Response=f"\nLLM: I tried to make a recipe, but we don't have enough ingredients. {validation_msg}\n"
                        messages.append({"role": "assistant", "content": f"Failed: {validation_msg}"})
                            
            else:
                Response=f"\nLLM: {raw_response}\n"
                messages.append({"role": "assistant", "content": raw_response})
                break
            
            
    db.close()
    return render_template(
        "InventoryPage.html",
        items=items,
        current_player=current_player,
        Response=Response
    )


# =====================
# Add Item Page
# =====================
from unit_conversion import normalize_quantity

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_item_page():
    player_id = session["player_id"]

    if request.method == "POST":
        db = get_db()

        name = request.form["name"].lower().strip()
        # basic check to further prevent plural input for inventory item names
        if name.endswith(("s", "es", "ies")):
            flash("Plural ingredient names are not allowed. Use singular form.")
            return redirect(url_for("add_item"))
        
        category = request.form.get("category", "other")
        quantity = int(request.form["quantity"])
        unit = request.form.get("unit", "each")
        measurement_type = request.form.get("measurement_type", "count")
        purchase_date = request.form.get("purchase_date")
        best_by = request.form.get("best_by")
        opened = 1 if request.form.get("opened") else 0
        price = float(request.form.get("price", 0.0))
        status = "active"

        # Convert units using your file
        grams, ml = normalize_quantity(quantity, unit, measurement_type)

        # Calculate flags automatically
        item_dict = {
            "name": name,
            "category": category,
            "best_by": best_by,
            "opened": opened
        }

        raw_meat, perishable, donation_allowed, decomposition_flag = calculate_flags(item_dict)

        db.execute("""
            INSERT INTO inventory (
                player_id, name, category, quantity, unit, measurement_type,
                quantity_grams, quantity_ml,
                purchase_date, best_by,
                raw_meat, perishable, opened,
                donation_allowed, decomposition_flag,
                price, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            player_id, name, category, quantity, unit, measurement_type,
            grams, ml,
            purchase_date, best_by,
            raw_meat, perishable, opened,
            donation_allowed, decomposition_flag,
            price, status
        ))

        db.execute("""
            UPDATE players SET score = ROUND(score + ?, 2)
            WHERE id = ?
        """, (price * quantity, player_id))

        db.commit()
        db.close()

        return redirect(url_for("inventory_page"))

    db = get_db()
    current_player = db.execute(
        "SELECT * FROM players WHERE id = ?", (player_id,)
    ).fetchone()
    db.close()

    return render_template("AddItemPage.html", current_player=current_player)

# =====================
# Use Item
# =====================
@app.route("/use/<int:item_id>", methods=["POST"])
@login_required
def use_item(item_id):
    player_id = session["player_id"]
    db = get_db()

    item = db.execute(
        "SELECT quantity, price FROM inventory WHERE id = ?",
        (item_id,)
    ).fetchone()

    if item:
        new_qty = item["quantity"] - 1

        if new_qty <= 0:
            db.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
        else:
            db.execute(
                "UPDATE inventory SET quantity = ? WHERE id = ?",
                (new_qty, item_id)
            )

        db.execute(
            "UPDATE players SET score = score - ? WHERE id = ?",
            (item["price"], player_id)
        )

        db.commit()

    db.close()
    return redirect(url_for("inventory_page"))

# =====================
# Donate Item
# =====================
@app.route("/donate/<int:item_id>", methods=["POST"])
@login_required
def donate_item(item_id):
    player_id = session["player_id"]
    db = get_db()

    item = db.execute(
        "SELECT price FROM inventory WHERE id = ?",
        (item_id,)
    ).fetchone()

    if item:
        db.execute(
            "UPDATE players SET score = score - ? WHERE id = ?",
            (item["price"] * 0.5, player_id)
        )

        db.execute("UPDATE inventory SET status = 'donated' WHERE id = ?", (item_id,))
        db.commit()

    db.close()
    return redirect(url_for("inventory_page"))

# =====================
# Compost Item
# =====================
@app.route("/compost/<int:item_id>", methods=["POST"])
@login_required
def compost_item(item_id):
    player_id = session["player_id"]
    db = get_db()

    item = db.execute(
        "SELECT price FROM inventory WHERE id = ?",
        (item_id,)
    ).fetchone()

    if item:
        db.execute(
            "UPDATE players SET score = score - ? WHERE id = ?",
            (item["price"] * 0.25, player_id)
        )

        db.execute("UPDATE inventory SET status = 'composted' WHERE id = ?", (item_id,))
        db.commit()

    db.close()
    return redirect(url_for("inventory_page"))

# =====================
# Delete Item
# =====================
@app.route("/delete/<int:item_id>", methods=["POST"])
@login_required
def delete_item(item_id):
    db = get_db()
    db.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    db.commit()
    db.close()

    return redirect(url_for("inventory_page"))


# =====================
# Score Board  (we should rethink the scoring)
# =====================
@app.route("/scoreboard")
@login_required
def scoreboard():
    db = get_db()

    # Order by score ascending (ascending = lowest → highest)
    players = db.execute("""
        SELECT id, name, score, profile_picture
        FROM players
        ORDER BY score ASC
    """).fetchall()

    db.close()

    return render_template("ScoreboardPage.html", players=players)




# ==================================================================================================
# Saving Meal Recipe
# ==================================================================================================
@app.route("/save_meal", methods=["POST"])
@login_required
def save_meal():
    player_id = session["player_id"]
    recipe_text = request.form.get("recipe_text", "").strip()
    
    # =============================
    # Parse recipe
    # =============================
    lines = recipe_text.split("\n")
    name = lines[0].strip() if lines else "Untitled Recipe"
    ingredients = "\n".join(
        [line.strip() for line in lines if "-" in line or "•" in line]
    )
    description = recipe_text

    # ========================================================================
    # Insert to database
    # ========================================================================
    db = get_db()

    try:
        db.execute("""
            INSERT INTO meals (player_id, name, ingredients, description)
            VALUES (?, ?, ?, ?)
        """, (player_id, name, ingredients, description))

        db.commit()
    
    finally:
        db.close()
    # ==========================================================================
    flash("Recipe saved!", "success")
    return redirect(url_for("dashboard"))
# ==================================================================================================

# ==========================================================================================
# View Meal Recipe
# ==========================================================================================
@app.route("/meal/<int:meal_id>")
@login_required
def view_meal(meal_id):
    db = get_db()
    meal = db.execute(
        "SELECT * FROM meals WHERE id = ? AND player_id = ?",
        (meal_id, session["player_id"])
    ).fetchone()
    db.close()

    if meal is None:
        return "Meal not found", 404

    return render_template("ViewMeal.html", meal=meal)





# Citations:
# ----------
# dashboard implemented using a Google Gemini prompt as a guideline: 
# "I want to make it simple and have it show in text like a notification on the website for the player"

# =========================================================
# AI Menu
# =========================================================
#@app.route('/ai_menu/<int:player_id>')
#def ai_menu(player_id):
 #   db = get_db()

  #  current_player = db.execute("""
    #    SELECT * FROM players WHERE id = ?
  #  """, (player_id,)).fetchone()

  #  items = db.execute("""
    #    SELECT id, name, quantity
    #    FROM inventory
    #    WHERE player_id = ?
  #  """, (player_id,)).fetchall()

  #  inventory_list = [dict(item) for item in items]
#
   # messages = [
       # {
         #   "role": "system",
          #  "content": (
             #   "You are a cooking assistant. "
             #   "You MUST ONLY use ingredients from the provided inventory. "
              ##  "Do not invent ingredients. "
              #  "Create a menu of 3–5 dishes using ONLY these items."
              #  "If the ingredient is not available in the inventory it can not be used"
              #  "You may ONLY use ingredients from the provided inventory list."
               # "You may NOT invent, assume, or add any ingredient that is not explicitly listed."
               # "If an ingredient is missing, you must work around it."
              #  "You must create 3–5 dish ideas using ONLY the inventory items."
               # "Each dish must clearly list which inventory items it uses."
                #"If the inventory is too small to make full dishes, create simple snacks or combinations."
               # "Never mention these rules in your output."
               # "Do not under any circumstances add any ingredients."
               # "If there are no tortillas in the inventory do not suggest tacos."
               # "I would also like each suggestion to have a link to a fully detailed recipe."
               # "Assume that the user does not have spare money to buy extra ingredients and can only use what is in the inventory."
               # "You may NOT invent or assume ingredients that are not explicitly listed."
               # "If the inventory is small, create simple dishes using only what is available."
               # "Make each recipe suggestion it's own object to be stored in a database."
           # )
       # },
       # {
           # "role": "user",
           # "content": f"Here is the player's inventory:\n{inventory_list}"
       # }#
   # ]

    #response = requests.post(
  #  "https://openrouter.ai/api/v1/chat/completions",
    #headers={
    #    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
   #     "Content-Type": "application/json"
   # },
   # json={
     #   "model": "gryphe/mythomax-l2-13b",
     #   "messages": messages
  #  }
#).json()

    # print("AI RAW RESPONSE:", response) # For testing, prints what the AI replies in the terminal

  #  if "choices" not in response:
   #     return f"AI Error: {response}"

  #  ai_menu = response["choices"][0]["message"]["content"]

   # return render_template(
   ##     "AIMenuPage.html",
     #   menu=ai_menu,
   #     items=items,
    #    current_player=current_player
   # )
#

# ============================================================

# ======================
# Uncomment this section
# to serve over network
# ngrok http 5000
# ======================

#if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=5000)


# ======================
# Uncomment this section 
# to only serve locally
# ======================

if __name__ == "__main__":
    app.run(debug=True)

# ===============
# ngrok http 5000
# ===============

# ================
# for render.com
# gunicorn app:app
# ================







