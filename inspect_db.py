import sqlite3
import os

# Get the path to the database file in the "instance" directory
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'database.db')

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query the "instruments" table
cursor.execute("SELECT * FROM instruments")
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the database connection
conn.close()