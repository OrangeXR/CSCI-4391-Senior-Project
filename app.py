from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
import requests
import sqlite3
from datetime import datetime, timedelta
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from unit_conversion import normalize_quantity, convert_recipe_unit
from expiry import get_expiry_date, urgent_expiry_date
import json

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

# sustanability tier helper
def get_sustainability_tier(efficiency):
    if efficiency >= 90: return "Eco-Legend 🏆"
    if efficiency >= 75: return "Eco-Warrior 🛡️"
    if efficiency >= 50: return "Apprentice 🌱"
    return "Novice 🐣"

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
    player_id = session.get('player_id')
    expiring_soon = get_expiry_date(player_id)
    urgent_expiring_soon = urgent_expiry_date(player_id)

# =============================================================================================================
# Get a list of saved recipes for the user + get score and pfp for dashboard
# =============================================================================================================
    db = get_db()

    # new - fetch full player record so pfp and score can be shown on dashboard
    current_player = db.execute(
        "SELECT * FROM players WHERE id = ?", (player_id,)
    ).fetchone()

    # new - fetch inventory to calculate waste reduction flags
    inventory_items = db.execute(
        "SELECT * FROM inventory WHERE player_id = ? AND status = 'active'", 
        (player_id,)
    ).fetchall()

    # calculation logic for efficiency
    acquired = current_player['total_value_acquired'] or 0
    saved = current_player['total_value_saved'] or 0
    efficiency = (saved / acquired * 100) if acquired > 0 else 0

    # new - calculate stats for dashboard
    metrics = db.execute("""
        SELECT 
            SUM(CASE WHEN status = 'active' THEN price ELSE 0 END) as active_value,
            SUM(CASE WHEN status = 'donated' THEN price * 0.5 ELSE 0 END) as donated_impact,
            SUM(CASE WHEN status = 'composted' THEN price * 0.25 ELSE 0 END) as composted_impact
        FROM inventory 
        WHERE player_id = ?
    """, (player_id,)).fetchone()

    # initialize stats 
    stats = {
        "donation_eligible": 0,
        "expired_perishables": 0,
        "total_active": len(inventory_items),
        "active_value": metrics["active_value"] or 0,
        "donated_impact": metrics["donated_impact"] or 0,
        "composted_impact": metrics["composted_impact"] or 0
    }

    # loop thru active items to calculate donation eligibility and expired perishables for dashboard stats
    for item in inventory_items:
        # dict(item) ensures calculate_flags can read the keys correctly
        _, _, donation_allowed, decomposition = calculate_flags(dict(item))
        stats["donation_eligible"] += donation_allowed
        stats["expired_perishables"] += decomposition

    # fetch meals
    meals = db.execute(
        "SELECT id, name, created_at FROM meals WHERE player_id = ? ORDER BY created_at DESC",
        (player_id,)
    ).fetchall()
# =============================================================================================================
# =============================================================================================================

   # if not player:
        # if they aren't logged in, send them to the login page
       # return redirect('/login')
    
    if urgent_expiring_soon:
        item_list = ", ".join(urgent_expiring_soon)
        flash(f"Heads up! Your {item_list} will expire in 1 day!", "urgent")

    if expiring_soon:
        item_list = ", ".join(expiring_soon)
        flash(f"Heads up! Your {item_list} will expire in 4 days.", "warning")

    return render_template('dashboard.html', player=current_player, meals=meals, stats=stats, efficiency=round(efficiency, 1),
                            tier=get_sustainability_tier(efficiency))

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

        # Always update dietary fields
        db.execute(
            "UPDATE players SET food_allergies = ?, dietary_needs = ? WHERE id = ?",
            (food_allergies, dietary_needs, player_id)
        )

        # Only update picture if uploaded
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            db.execute(
                "UPDATE players SET profile_picture = ? WHERE id = ?",
                (filename, player_id)
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
        food_allergies = request.form.get("food_allergies")
        dietary_needs = request.form.get("dietary_needs")
        password = request.form["password"]
        file = request.files["profile_picture"]

        password_hash = generate_password_hash(password)

        filename = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        db = get_db()
        db.execute("""
            INSERT INTO players (name, username, password_hash, profile_picture, food_allergies, dietary_needs)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, username, password_hash, filename, food_allergies, dietary_needs))
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

# ========================================================
    # CALCULATE EFFICIENCY FOR THIS PAGE
    # ========================================================
    acquired = current_player['total_value_acquired'] or 0
    saved = current_player['total_value_saved'] or 0
    efficiency = (saved / acquired * 100) if acquired > 0 else 0
    tier = get_sustainability_tier(efficiency)
# =====================
# Ai integration 
# =====================
    Response = None     #So errors dont occur

    if request.method == 'POST': #Checking if any is inputed
        message = request.form.get("message", "hello")  #default message 
        user_lower = message.lower()

        Chat_box_In = Ai_Chat()  #creating an instance 
        Chat_validator = recipe_validator()
        inventory_items = Chat_box_In.get_active_inventory(player_id)  #getting context for the AI
        inventory_context = Chat_box_In.build_inventory_context(inventory_items)

        #Message for the AI same as openrouterllm
        messages = [
            {
                "role": "system",
                "content": (
                    "## ROLE\n"
                    "You are an eco-conscious Food Waste Reducer. Your goal is to create recipes "
                    "using ONLY provided inventory, prioritizing items marked [ABOUT TO EXPIRE].\n\n"
                    # --------------------------------------------------------------------------------------------
                    # Check allergies and dietary needs
                    # ---------------------------------------------------------------------------------------------
                    "## PLAYER DIET & ALLERGIES\n"
                    f"- Player food allergies: {current_player['food_allergies'] or 'None specified'}\n"
                    f"- Player dietary needs: {current_player['dietary_needs'] or 'None specified'}\n\n"
                    "- You MUST NOT include any ingredient that conflicts with the player's food allergies.\n"
                    "- You MUST respect the player's dietary needs when suggesting recipes.\n\n"
                    # ---------------------------------------------------------------------------------------------
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
                    "- Before the recipe steps, include a short line:\n"
                    "  'Diet Check: <how this recipe satisfies allergies & dietary needs>'\n"
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
                    "marked donation_allowed=1 that are NOT expired and NOT raw_meat. "
                    "No text before or after. No markdown.\n"
                    "{\n"
                    '  "response_type": "donation",\n'
                    '  "suggestions": [\n'
                    '    {\n'
                    '      "name": "string — item name exactly as in inventory",\n'
                    '      "quantity": number,\n'
                    '      "unit": "string — use the unit from inventory",\n'
                    '      "donation_tip": "string — REQUIRED, specific tip e.g. bring to food bank sealed, check best-by before drop-off, community fridge accepted"\n'
                    '    }\n'
                    '  ]\n'
                    "}\n"
                )
            }
        ]

        # append user message to conversation
        messages.append({"role": "system",
                          "content": f"Current Inventory:\n{inventory_context}" # provide current inventory context to the LLM every turn so it can make informed suggestions based on what the player has available
                         })
        
        messages.append({"role": "user", "content": message})

        MAX_RETRIES = 1 # retries for recipe generation if validation fails, can adjust as needed 
        #===============
        # Recipe section
        #===============
        if any(word in user_lower for word in Chat_box_In.Cook_WORDS):
            for attempt in range(MAX_RETRIES):
                raw_response = Chat_box_In.getLLMResponse(messages)
                # for rate limit exceeded 
                if raw_response is None:
                    Response = {"type": "error", "text": "The model is busy. Please try again in a moment."}
                    break
                # send recipe to validator
                is_valid, validation_msg = Chat_validator.validate_AI_recipe(raw_response, player_id, current_player)
                if is_valid:
                    try:
                        raw_response = raw_response.strip()
                        #parsed = json.loads(raw_response)
                        #extract JSON safely
                        start = raw_response.find("{")
                        end = raw_response.rfind("}") + 1
                        json_str = raw_response[start:end]

                        parsed= json.loads(json_str)

                        session["last_recipe"] = parsed
                        used_ingredients = parsed.get("ingredients_used", []) 
                        Response = {
                            "type": "recipe",
                            "title": parsed.get("recipe_title", "Recipe"),
                            "ingredients": used_ingredients,
                            "steps": validation_msg["recipe_text"],
                            "diet": validation_msg["diet_summary"]
                        }
                            
                    except json.JSONDecodeError:
                        Response = {"type": "chat", "text": raw_response}
                        break
                else:
                    Response = {"type": "error", "text": f"I tried to make a recipe with your current inventory. {validation_msg}"}
        
        # ================
        # donation section
        # ================
        elif any(word in user_lower for word in Chat_box_In.Donate_WORDS):
            for attempt in range(MAX_RETRIES):
                raw_response = Chat_box_In.getLLMResponse(messages)
                if raw_response is None:
                    Response = {"type": "error", "text": "The model is busy. Please try again in a moment."}
                    break
                try:
                    parsed = json.loads(raw_response)
                    if "suggestions" not in parsed:
                        raise ValueError("Missing suggestions key")
                    suggestions = parsed.get("suggestions", [])
                    Response = {"type": "donation", "suggestions": suggestions}      
                    break
                except (json.JSONDecodeError, ValueError):
                    if attempt < MAX_RETRIES:
                        messages.append({"role": "assistant", "content": raw_response})
                        messages.append({"role": "user", "content": "Return ONLY valid JSON with a 'suggestions' list for donation. No explanation. Follow the schema exactly."})
                    else:
                        Response = {"type": "chat", "text": raw_response}

        # =====================
        # decomposition section
        # =====================
        elif any(word in user_lower for word in Chat_box_In.Decomp_WORDS):
            for attempt in range(MAX_RETRIES):
                raw_response = Chat_box_In.getLLMResponse(messages)
                if raw_response is None:
                    Response = {"type": "error", "text": "The model is busy. Please try again in a moment."}
                    break
                try:
                    parsed = json.loads(raw_response)
                    if "suggestions" not in parsed:
                        raise ValueError("Missing suggestions key")
                    
                    Response = {"type": "decomposition", "suggestions": parsed.get("suggestions", [])}
                    break
                except (json.JSONDecodeError, ValueError):
                    if attempt < MAX_RETRIES:
                        messages.append({"role": "assistant", "content": raw_response})
                        messages.append({"role": "user", "content": "Return ONLY valid JSON with a 'suggestions' list for decomposition. No explanation. Follow the schema exactly."})
                    else:
                        Response = {"type": "chat", "text": raw_response}

        # ============
        # general chat
        # ============
        else:
            raw_response = Chat_box_In.getLLMResponse(messages)
            if raw_response is None:
                Response = {"type": "error", "text": "The model is busy. Please try again in a moment."}
            else:
                Response = {"type": "chat", "text": raw_response}  
    db.close()
    return render_template(
        "InventoryPage.html",
        items=items,
        current_player=current_player,
        Response=Response,
        efficiency=round(efficiency, 1),
        tier=tier
    )
    
#apply recipe amount used (when "Cook this recipe is clicked")
@app.route("/apply_recipe", methods=["POST"])
@login_required
def apply_recipe():
    player_id = session["player_id"]
    db = get_db()

    recipe = session.get("last_recipe")

    if not recipe:
        return redirect(url_for("inventory_page"))

    total_score_change = 0
    saved_value = 0

    for ing in recipe.get("ingredients_used", []):
        item = db.execute(
            "SELECT * FROM inventory WHERE name = ? AND player_id = ?",
            (ing["name"], player_id)
        ).fetchone()

        if not item:
            continue

        amount, _ = convert_recipe_unit(ing["quantity"], ing["unit"])

        base_qty = item["quantity_grams"] or item["quantity_ml"] or item["quantity"]

        if base_qty and base_qty > 0:
            usage_ratio = min(amount / base_qty, 1) 
            score_change= item["price"] * usage_ratio
            total_score_change += score_change
            saved_value += score_change
        consume_inventory_item(db, item, amount, ing["unit"])

    db.execute(
        "UPDATE players SET score = ROUND(score - ?, 2), total_value_saved = total_value_saved + ? WHERE id = ?", # round to 2 decimals
        (total_score_change, saved_value, player_id)
    )

    db.commit()
    db.close()
    flash(f"Recipe cooked successfully! -{total_score_change:.2f} points used (ingredients used efficiently).", "success")

    return redirect(url_for("inventory_page"))

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

        total_price = price * quantity # calculate total price based on quantity added
        db.execute("""
            UPDATE players 
            SET score = ROUND(score + ?, 2), 
                total_value_acquired = total_value_acquired + ? 
            WHERE id = ?
        """, (total_price, total_price, player_id)) # update score and total value acquired for player when adding items, round score to 2 decimals

        db.commit()
        db.close()

        return redirect(url_for("inventory_page"))

    db = get_db()
    current_player = db.execute(
        "SELECT * FROM players WHERE id = ?", (player_id,)
    ).fetchone()
    db.close()

    return render_template("AddItemPage.html", current_player=current_player)



# =====================================
# update inventory if user uses recipe
# ======================================
def consume_inventory_item(db, item, amount, unit):

    grams = item["quantity_grams"]
    ml = item["quantity_ml"]

    unit = unit.lower()

    # ====================
    # weight consumption
    # ====================
    if unit in ["g", "gram", "grams", "kg", "lb", "oz", "mg"]:
        if grams is None:
            return False

        new_value = grams - amount

        if new_value <= 0:
            db.execute("DELETE FROM inventory WHERE id = ?", (item["id"],))
        else:
            db.execute(
                "UPDATE inventory SET quantity_grams = ? WHERE id = ?",
                (new_value, item["id"])
            )

    # ====================
    # volume consumption
    # ====================
    elif unit in ["ml", "l", "liter", "cup", "tbsp", "tsp", "fl_oz", "gallon"]:
        if ml is None:
            return False

        new_value = ml - amount

        if new_value <= 0:
            db.execute("DELETE FROM inventory WHERE id = ?", (item["id"],))
        else:
            db.execute(
                "UPDATE inventory SET quantity_ml = ? WHERE id = ?",
                (new_value, item["id"])
            )

    # ====================
    # count items 
    # ====================
    else:
        new_value = item["quantity"] - amount

        if new_value <= 0:
            db.execute("DELETE FROM inventory WHERE id = ?", (item["id"],))
        else:
            db.execute(
                "UPDATE inventory SET quantity = ? WHERE id = ?",
                (new_value, item["id"])
            )

    return True
# =====================
# Use Item
# =====================
@app.route("/use/<int:item_id>", methods=["POST"])
@login_required
def use_item(item_id):
    player_id = session["player_id"]
    db = get_db()

    item = db.execute(
        "SELECT name, quantity, price FROM inventory WHERE id = ?",
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

        score_change = item["price"]

        db.execute(
            "UPDATE players SET score = ROUND(score - ?, 2), total_value_saved = total_value_saved + ? WHERE id = ?",
            (score_change, score_change, player_id)
        )

        flash(f"Used {item['name']}! -{score_change:.2f} points (consumed efficiently).", "success")

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
        # <--- UPDATED FOR EFFICIENCY MODEL: Add to saved
        score_change = item["price"] * 0.5
        db.execute(
            "UPDATE players SET score = ROUND(score - ?, 2), total_value_saved = total_value_saved + ? WHERE id = ?",
            (score_change, item["price"], player_id)
        )

        flash(f"Donated item! -{score_change:.2f} points (helped others & reduced waste).", "success")

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

    if item: # add to saved
        score_change = item["price"] * 0.25

        db.execute(
            "UPDATE players SET score = ROUND(score - ?, 2), total_value_saved = total_value_saved + ? WHERE id = ?",
            (score_change, item["price"], player_id)
        )

        flash(f"Composted item! -{score_change:.2f} points (waste reduced sustainably).", "success")

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
    player_id = session["player_id"]
    db = get_db()

    item = db.execute(
        "SELECT price, status, name FROM inventory WHERE id = ?",
        (item_id,)
    ).fetchone()

    if item:
        status = item["status"] if "status" in item.keys() else "active"

        #penalize ONLY if not already handled properly
        if status not in ["composted", "donated"]:
            penalty = item["price"] * 1.0
            db.execute(
                "UPDATE players SET score = ROUND(score + ?, 2) WHERE id = ?", # round to 2 decimals
                (penalty, player_id)
            )
            flash(f"+{penalty:.2f} points for wasting food!", "error")
        else: 
            #feedback for composted/donated delete action
            flash(f"{item['name']} successfully removed from inventory.", "success")
            
    db.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    db.commit()
    db.close()

    return redirect(url_for("inventory_page"))

# ==============
# delete recipe
# ==============
@app.route("/delete_meal/<int:meal_id>", methods=["POST"])
@login_required
def delete_meal(meal_id):
    db = get_db()

    meal = db.execute(
        "SELECT name FROM meals WHERE id = ?",
        (meal_id,)
    ).fetchone()

    if meal:
        db.execute("DELETE FROM meals WHERE id = ?", (meal_id,))
        db.commit()
        flash(f"{meal['name']} deleted successfully.", "success")

    db.close()
    return redirect(url_for("dashboard"))  

# =====================
# Score Board  (we should rethink the scoring)
# =====================
@app.route("/scoreboard")
@login_required
def scoreboard():
    db = get_db()

    # Order by score ascending to show top performers at the top of the scoreboard
    players = db.execute("""
        SELECT id, name, profile_picture,
               (total_value_saved / NULLIF(total_value_acquired, 0)) * 100 AS efficiency
        FROM players
        ORDER BY efficiency DESC
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
    recipe= session.get("last_recipe")

    if not recipe: 
        flash("No recipe to save.", "error")
        return redirect(url_for("inventory_page"))
    
    name = recipe.get("recipe_title", "Untitled Recipe")
    ingredients = "\n".join([
        f"{ing['name']} - {ing['quantity']} {ing['unit']}"
        for ing in recipe.get("ingredients_used", [])
    ])

    description = recipe.get("recipe_text", "")

    db= get_db()
    try:
        db.execute("""
            INSERT INTO meals (player_id, name, ingredients, description)
            VALUES (?, ?, ?, ?)
        """, (player_id, name, ingredients, description))

        db.commit()
    finally: 
        db.close()
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







