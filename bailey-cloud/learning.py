import sqlite3

conn = sqlite3.connect("bailey.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clone_id TEXT,
    user TEXT,
    message TEXT,
    reply TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def log_interaction(user, message, reply, clone_id):
    cursor.execute(
        "INSERT INTO interactions (clone_id, user, message, reply) VALUES (?, ?, ?, ?)",
        (clone_id, user, message, reply)
    )
    conn.commit()
