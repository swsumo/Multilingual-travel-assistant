import sqlite3

def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
