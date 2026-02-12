from flask import Flask, render_template, request, redirect
from models import get_all_items, add_item

''' ======================== 
    Create Flask application 
    ======================== '''
app = Flask(__name__)

''' ========= 
    Home Page  
    ========= '''
@app.route("/")
def home_page():
    return render_template("HomePage.html") # First page user sees when visiting site

''' =======================
    Other Pages can go here
    ======================= '''

''' ================================= 
    Pulls data from db and stores it
    getting ready for use in template
    ================================= '''

@app.route("/inventory")
def inventory_page():
    items = get_all_items() # <--------------------------------- info stored in 'items'
    return render_template("InventoryPage.html", items=items)

@app.route("/add", methods=["GET", "POST"]) # <----------------- GET gets the form and returns it on line 41
def add_item_page():
    if request.method == "POST": # <---------------------------- P0ST reads the form the user filled out 
        data = { # <-------------------------------------------- Builds a dictionary from the entry
            "name": request.form["name"],
            "category": request.form["category"],
            "quantity": request.form["quantity"],
            "best_by": request.form["best_by"]
        }
        add_item(data)  # <------------------------------------- Data is inserted into db
        return redirect("/inventory") # <----------------------- Redirects user have to inventory
    return render_template("AddItemPage.html") # <-------------- AddItemPage.html

# -------------------- Run App --------------------
if __name__ == '__main__':
    app.run(debug=True)
