import sqlite3

from langchain.tools import tool


@tool
def get_existing_flowers():
    """
    Used to retrieve flowers that are present in flower shop.
    First digital value is price.
    Second digital value is delivery cost.
    """

    conn = sqlite3.connect('flowers.db')
    cursor = conn.cursor()

    # Retrieve all entries from the 'flowers' table
    cursor.execute('SELECT * FROM flowers')
    flowers = cursor.fetchall()

    conn.close()

    return flowers
