import sqlite3

DB_FILE = "inventory.db"

with sqlite3.connect(DB_FILE) as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        name TEXT NOT NULL,
        date_added TEXT NOT NULL, 
        quantity INTRGER,
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
        time_changed TEXTS
        )
    """)

    