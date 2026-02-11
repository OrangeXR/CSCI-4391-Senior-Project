from flask import Flask, render_template, request, redirect
from models import get_all_items, add_item

app = Flask(__name__)

# -------------------- Home Page --------------------
@app.route("/")
def home_page():
    return render_template("HomePage.html")

# -------------------- Other Page can go here --------------------
@app.route("/inventory")
def inventory_page():
    items = get_all_items()
    return render_template("InventoryPage.html", items=items)

@app.route("/add", methods=["GET", "POST"])
def add_item_page():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "category": request.form["category"],
            "quantity": request.form["quantity"],
            "best_by": request.form["best_by"]
        }
        add_item(data)
        return redirect("/inventory")
    return render_template("AddItemPage.html")

# -------------------- Run App --------------------
if __name__ == '__main__':
    app.run(debug=True)
