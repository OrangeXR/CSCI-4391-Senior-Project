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
