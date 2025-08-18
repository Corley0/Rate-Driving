import sqlite3
from datetime import datetime
#from flask_login import UserMixin

DB_PATH = 'app.db'
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def get_timestamp():
    now = datetime.now()
    timestamp = now.timestamp()
    return int(timestamp)

def create_db():
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT,
        creation_timestamp INTEGER,
        permission_level INTEGER,
        account_verified INTEGER
    )
    ''')

    # Create reviews table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        author_id INTEGER,
        plate TEXT,
        description TEXT,
        rating INTEGER,
        creation_timestamp INTEGER,
        FOREIGN KEY (author_id) REFERENCES users (user_id)
    )
    ''')

    # Create comments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        author_id INTEGER,
        review_id INTEGER,
        description TEXT,
        creation_timestamp INTEGER,
        FOREIGN KEY (author_id) REFERENCES users (user_id),
        FOREIGN KEY (review_id) REFERENCES reviews (review_id)
    )
    ''')

    conn.commit()

def add_user(username: str, email: str, password: str, permission_level: int = 1):
    cursor.execute('''
    INSERT INTO users (username, email, password, creation_timestamp, permission_level)
    VALUES (?, ?, ?, ?, ?)
''', (username, email, password, get_timestamp(), permission_level))
    conn.commit()