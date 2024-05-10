import sqlite3


def create_db():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('flowers.db')
    cursor = conn.cursor()

    cursor.execute('''
CREATE TABLE IF NOT EXISTS flowers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    delivery_cost REAL,
    color TEXT NOT NULL
)
''')

    conn.commit()
    conn.close()
    print("Table 'flowers' created successfully.")