from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# ========================
# Create Flask application
# ========================
app = Flask(__name__)
app.secret_key = "super-secret-key"

UPLOAD_FOLDER = "src/static/profile_pics"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# =============
# Connect to db
# =============
def get_db():
    conn = sqlite3.connect("src/instance/inventory.db")
    conn.row_factory = sqlite3.Row
    return conn

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

# =====================
# User Profile
# =====================
#@app.route("/userprofile")
#@login_required
#def profile():
#    player_id = session["player_id"]
#    db = get_db()

#    current_player = db.execute("SELECT * FROM players WHERE id = ?", (session["player_id"],)).fetchone()
#    db.close()

#    return render_template("UserProfile.html", current_player=current_player)


@app.route("/userprofile", methods=["GET", "POST"])
@login_required
def userprofile():
    player_id = session["player_id"]
    db = get_db()

# ========================================================================= Change profile pic upload
    if request.method == "POST":
        file = request.files.get("profile_picture")

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join("static/profile_pics", filename)
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


# ==========================================
# Inventory Page (uses logged-in player)
# ==========================================
@app.route("/inventory")
@login_required
def inventory_page():
    player_id = session["player_id"]

    db = get_db()
    current_player = db.execute(
        "SELECT * FROM players WHERE id = ?", (player_id,)
    ).fetchone()

    items = db.execute(
        "SELECT * FROM inventory WHERE player_id = ? ORDER BY best_by ASC",
        (player_id,)
    ).fetchall()

    db.close()

    return render_template(
        "InventoryPage.html",
        items=items,
        current_player=current_player
    )

# =====================
# Add Item Page
# =====================
@app.route("/add", methods=["GET", "POST"])
@login_required
def add_item_page():
    player_id = session["player_id"]

    if request.method == "POST":
        db = get_db()

        name = request.form["name"]
        category = request.form["category"]
        quantity = int(request.form["quantity"])
        best_by = request.form["best_by"]
        price = float(request.form["price"])

        db.execute("""
            INSERT INTO inventory (player_id, name, category, quantity, best_by, price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (player_id, name, category, quantity, best_by, price))

        db.execute("""
            UPDATE players SET score = score + ?
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