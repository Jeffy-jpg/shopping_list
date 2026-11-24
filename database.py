import sqlite3

DB_FILE = "inventory.db"

with sqlite3.connect(DB_FILE) as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        name TEXT NOT NULL,
        date_added TEXT NOT NULL, 
        quantity INTEGER,
        price REAL)        
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXIST item_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id TEXT NOT NULL,
        adjust_method TEXT,
        total_difference INTERGER
        new_fig INTEGER 
        comment TEXT
        date_updated TEXT
        )
    """)

def save_all(shopping_data, item_history):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()

        cur.execute("DELETE FRORM inventory")
        inventory_rows = [
            (
            category,
            item ["name"], 
            item.get("date_added", ""), 
            item ["quantity"],
            item ["price"] 
            )
            for category, items in shopping_data.items()
            for item in items
        ]
        cur.executemany("""
        INSERT INTO inventory
        (category, name, date_added, quantity, price)
        VALUES  (?,?,?,?,?)""", inventory_rows)

        cur.execute("DELETE FROM item_history")
        history_rows = [
              (
                  item_id,
                  entry["adj_methof"]
                  entry["difference"]
                  entry["new_figure"]
                  entry["comment"]
                  entry["date_updated"]

        for item_id, entries in item_history.items ()
        for entry in entries