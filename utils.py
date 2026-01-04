import sqlite3
import os

class PersistenceManager:
    def __init__(self, db_path='database/grit_browser.db'):
        self.db_path = db_path
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS session
                     (id INTEGER PRIMARY KEY, last_url TEXT, notes TEXT, xp INTEGER, streak INTEGER)''')
        conn.commit()
        conn.close()

    def save_session(self, url, notes, xp, streak):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO session (id, last_url, notes, xp, streak) VALUES (1, ?, ?, ?, ?)",
                  (url, notes, xp, streak))
        conn.commit()
        conn.close()

    def load_session(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT last_url, notes, xp, streak FROM session WHERE id=1")
        row = c.fetchone()
        conn.close()
        return row if row else (None, None, 0, 0)
