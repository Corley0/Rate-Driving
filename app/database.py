import sqlite3
from datetime import datetime
from app import login
from flask_login import UserMixin

DB_PATH = 'app.db'



def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def get_timestamp():
    now = datetime.now()
    timestamp = now.timestamp()
    return int(timestamp)

def create_db():
    conn = get_connection()
    cursor = conn.cursor()
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
    conn.close()

def add_user(username: str, email: str, password: str, permission_level: int = 1):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, email, password, creation_timestamp, permission_level) VALUES (?, ?, ?, ?, ?)', (username, email, password, get_timestamp(), permission_level))
    conn.commit()

def add_post(author_id: int, plate: str, description: str, rating: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reviews (author_id, plate, description, rating, creation_timestamp) VALUES (?, ?, ?, ?, ?)', (author_id, plate, description, rating, get_timestamp()))
    conn.commit()

def update_permissions(user_id: int, amount: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT permission_level FROM users WHERE user_id = (?)", (user_id,))
    current_perms = cursor.fetchone()[0]
    cursor.execute('UPDATE users SET permission_level = ? WHERE user_id = ?', (current_perms+amount, user_id))
    conn.commit()

def remove_account(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = (?)", (user_id,))
    conn.commit()

def remove_post(review_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reviews WHERE review_id = (?)", (review_id,))
    conn.commit()

def user_exists(username, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = ? OR email = ?", (username, email))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = str(id)
        self.email = email
        self.password = password
        self.authenticated = False
    
    def is_active(self):
        return self.is_active()
    
    def is_anonymous(self):
        return self.is_anonymous()
    
    def is_authenticated(self):
        return self.authenticated
    
    def is_active(self):
        return True

    def get_id(self):
        return self.id

create_db()

@login.user_loader
def load_user(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, email, password FROM users WHERE user_id = (?)",[id])
    data = cursor.fetchone()
    if data is None:
        return None
    else:
        return User(int(data[0]), data[1], data[2])