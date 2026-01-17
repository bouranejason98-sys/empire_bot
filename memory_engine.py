import sqlite3
from datetime import datetime

DB_PATH = "empire.db"

class MemoryEngine:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        # User memory table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            clone TEXT,
            last_intent TEXT,
            last_message TEXT,
            confidence REAL,
            timestamp TEXT
        )
        """)
        # Message logs table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            clone TEXT,
            message TEXT,
            reply TEXT,
            timestamp TEXT
        )
        """)
        # Clone registry table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clones (
            id TEXT PRIMARY KEY,
            region TEXT,
            niche TEXT,
            created_at TEXT
        )
        """)
        self.conn.commit()

    def remember(self, user, clone, intent, message, confidence):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO user_memory (user, clone, last_intent, last_message, confidence, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user, clone, intent, message, confidence, datetime.utcnow().isoformat()))
        self.conn.commit()

    def recall(self, user, clone):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT last_intent, last_message, confidence
        FROM user_memory
        WHERE user=? AND clone=?
        ORDER BY id DESC LIMIT 1
        """, (user, clone))
        row = cursor.fetchone()
        if row:
            return {"intent": row[0], "message": row[1], "confidence": row[2]}
        return None

    def log_message(self, user, clone, message, reply):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO messages (user, clone, message, reply, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """, (user, clone, message, reply, datetime.utcnow().isoformat()))
        self.conn.commit()

    def prune_memory(self, max_records=1000):
        cursor = self.conn.cursor()
        cursor.execute("""
        DELETE FROM user_memory
        WHERE id NOT IN (
            SELECT id FROM user_memory
            ORDER BY id DESC
            LIMIT ?
        )
        """, (max_records,))
        self.conn.commit()
