from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# ======================== 
# Create Flask application 
# ======================== 
app = Flask(__name__)

# ============= 
# Connect to db  
# =============
def get_db():
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row
    return conn

# ========= 
# Home Page  
# =========
@app.route("/", methods=["GET"])
def home_page():
    db = get_db()
    players = db.execute("SELECT * FROM players").fetchall()

    player_id = request.args.get("player_id")
    if not player_id and players:
        player_id = players[0]["id"]

    current_player = None
    if player_id:
        current_player = db.execute(
            "SELECT * FROM players WHERE id = ?", (player_id,)
        ).fetchone()

    db.close()

    return render_template(
        "HomePage.html",
        players=players,
        current_player=current_player
    )


# ========================================== 
# Pulls data from db per "player" and stores 
# it getting ready for use in template  
# ==========================================
@app.route("/inventory")
def inventory_page():
    player_id = request.args.get("player_id")
    if not player_id:
        return redirect("/")

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


@app.route("/add", methods=["GET", "POST"]) # <--------------------------------------------- GET gets the form and returns it on line 108
def add_item_page():
    player_id = request.args.get("player_id")

    if request.method == "POST": # <-------------------------------------------------------- P0ST reads the form the user filled out
        db = get_db()

        player_id = request.form["player_id"]
        name = request.form["name"]
        category = request.form["category"]
        quantity = int(request.form["quantity"]) # <-------- convert str to int
        best_by = request.form["best_by"]
        price = float(request.form["price"]) # <------------ convert int to float

        db.execute("""
            INSERT INTO inventory (player_id, name, category, quantity, best_by, price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (player_id, name, category, quantity, best_by, price)) # <--------------------- inserts values to  inventory.db along with current player

        db.execute("""
            UPDATE players SET score = score + ?
            WHERE id = ?
        """, (price * quantity, player_id)) # <--------------------------------------------- SCORE!!!

        db.commit()
        db.close()

        return redirect(url_for("inventory_page", player_id=player_id)) # <----------------- Redirects user have to inventory (for current player)

    db = get_db()
    current_player = db.execute(
        "SELECT * FROM players WHERE id = ?", (player_id,)
    ).fetchone()
    db.close()

    return render_template("AddItemPage.html", current_player=current_player) # <----------- GET gets the form and returns it on line 41 (for current player)


@app.route("/use/<int:item_id>/<int:player_id>", methods=["POST"]) # <---------------------- pulls infro from URL and passes it to function to use
def use_item(item_id, player_id):
    db = get_db()

    item = db.execute(# <------------------------------------------------------------------- checks to see if the item exists bye the id
        "SELECT quantity, price FROM inventory WHERE id = ?",
        (item_id,)
    ).fetchone()

    if item: # <---------------------------------------------------------------------------- If the item exixts
        new_qty = item["quantity"] - 1

        if new_qty <= 0: # <---------------------------------------------------------------- If the new quantity is 0 or less, delete from inventory
            db.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
        else:
            db.execute( # <----------------------------------------------------------------- otherwise update the quantity with new quantity
                "UPDATE inventory SET quantity = ? WHERE id = ?",
                (new_qty, item_id)
            )

        db.execute( # <--------------------------------------------------------------------- using the item reduces the player's "score" 
            "UPDATE players SET score = score - ? WHERE id = ?",
            (item["price"], player_id)
        )

        db.commit()

    db.close()# <--------------------------------------------------------------------------- close database and return to the player inventory
    return redirect(url_for("inventory_page", player_id=player_id))


@app.route("/donate/<int:item_id>/<int:player_id>", methods=["POST"]) # <------------------- Donating an item
def donate_item(item_id, player_id):
    db = get_db()

    item = db.execute(
        "SELECT price FROM inventory WHERE id = ?",
        (item_id,)
    ).fetchone()

    if item:
        db.execute(
            "UPDATE players SET score = score - ? WHERE id = ?", # <------------------------ if the item exists, get the item price * 0.5 (value of donating item) 
            (item["price"] * 0.5, player_id)
        )

        db.execute("UPDATE inventory SET status = 'donated' WHERE id = ?", (item_id,)) # <-- changes the status of the item to donated and commits the score and status change to the db (you'll be able to delete the item)
        db.commit() # <--------------------------------------------------------------------- (you'll be able to delete the item and still have the score change applied to total score)

    db.close() # <-------------------------------------------------------------------------- disconnect from db and return to player inventory
    return redirect(url_for("inventory_page", player_id=player_id))


@app.route("/compost/<int:item_id>/<int:player_id>", methods=["POST"]) 
def compost_item(item_id, player_id):
    db = get_db()

    item = db.execute( # <------------------------------------------------------------------ get the item's price
        "SELECT price FROM inventory WHERE id = ?",
        (item_id,)
    ).fetchone()

    if item: # <---------------------------------------------------------------------------- if the item exists and the player composts it, they get a bonus, but less than donating (price * 0.25) 
        db.execute(
            "UPDATE players SET score = score - ? WHERE id = ?",
            (item["price"] * 0.25, player_id)
        )

        db.execute("UPDATE inventory SET status = 'composted' WHERE id = ?", (item_id,))
        db.commit()

    db.close()
    return redirect(url_for("inventory_page", player_id=player_id))


@app.route("/delete/<int:item_id>/<int:player_id>", methods=["POST"]) # <------------------- Deleting an item
def delete_item(item_id, player_id):
    db = get_db()
    db.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    db.commit()
    db.close()

    return redirect(url_for("inventory_page", player_id=player_id))


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