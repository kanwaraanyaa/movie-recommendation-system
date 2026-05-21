import sqlite3
import bcrypt

# Connect database
def connect_db():
    return sqlite3.connect('users.db')

# Create user
def add_user(username, email, password):

    conn = connect_db()

    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )

        conn.commit()

        return True

    except:
        return False

# Verify login
def login_user(username, password):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    result = cursor.fetchone()

    if result:

        stored_password = result[0]

        if bcrypt.checkpw(
            password.encode('utf-8'),
            stored_password
        ):
            return True

    return False