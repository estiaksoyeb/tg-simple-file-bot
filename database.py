import sqlite3

# SQLite database file
DATABASE_FILE = "bot_database.db"

# Function to initialize the database
def init_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            short_id TEXT PRIMARY KEY,
            file_id TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Function to store a file_id in the database
def store_file_id(short_id, file_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO files (short_id, file_id) VALUES (?, ?)", (short_id, file_id))
    conn.commit()
    conn.close()

# Function to retrieve a file_id from the database
def get_file_id(short_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT file_id FROM files WHERE short_id = ?", (short_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None