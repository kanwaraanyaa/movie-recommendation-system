import sqlite3

# Connect database
conn = sqlite3.connect('users.db')

cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT,
    password TEXT
)
""")

conn.commit()

conn.close()

print("Database created successfully!")