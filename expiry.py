from database import get_db
from datetime import datetime, timedelta

def get_expiry_date(player_id):
    conn = get_db()
    cursor = conn.cursor()

    # calculate the date 4 days before expire
    target_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
    query = "SELECT name FROM inventory WHERE player_id = ? AND best_by = ? AND status = 'active'"
    cursor.execute(query, (player_id, target_date))
    items = cursor.fetchall()
    conn.close

    return [item['name'] for item in items]

def sort_inventory(player_id):
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT name, best_by FROM inventory"
    cursor.execute(query)
    items = cursor.fetchall()
    conn.close

    # store sorted inventory
    expired = []
    about_to_expire = []
    fresh = []

    today = datetime.now()

    # sorting by expired, about to expire, and fresh
    for item in items:
        expiry_date = datetime.strptime(item['best_by'], '%Y-%m-%d')
        days_left = (expiry_date - today).days

        if days_left < 0:
            expired.append(item['name'])
        elif days_left <= 4:
            about_to_expire.append(item['name'])
        else:
            fresh.append(item['name'])

    return expired, about_to_expire, fresh

# Citations:
# ---------
# get_expiry_date() implemented using a Google Gemini prompt as a guideline:
# "I want to make it simple and have it show in text like a notification on the website for the player"
# sort_inventory() : "cant i just make a function that sorts expired items and items about to expire and non expired"

