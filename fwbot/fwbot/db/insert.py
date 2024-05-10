import sqlite3


def insert_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('flowers.db')
    cursor = conn.cursor()

    # Data to be inserted
    flowers_data = [
        ('Rose', 10.50, 14.50, 'Red'),
        ('Tulip', 7.25, 11.25, 'Yellow'),
        ('Orchid', 20.00, 24.00, 'White'),
        ('Daisy', 5.00, 9.00, 'Blue'),
        ('Lily', 15.75, 19.75, 'Pink')
    ]

    # Insert the data into the 'flowers' table
    cursor.executemany('''
    INSERT INTO flowers (name, price, delivery_cost, color)
    VALUES (?, ?, ?, ?)
    ''', flowers_data)

    conn.commit()
    conn.close()

    print("Data inserted successfully.")
