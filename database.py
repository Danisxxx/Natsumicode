import sqlite3

KEY_DB_PATH = 'Key.db'
CLAIM_DB_PATH = 'Claim.db'
ERROR_DB_PATH = 'errors.db'

def save_key(key, plan, days, expiration):
    """Guarda una nueva llave en Key.db."""
    with sqlite3.connect(KEY_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keys (
                key TEXT PRIMARY KEY,
                plan TEXT,
                days INTEGER,
                expiration DATETIME,
                claimed BOOLEAN DEFAULT 0
            )
        ''')
        cursor.execute('''
            INSERT OR REPLACE INTO keys (key, plan, days, expiration, claimed)
            VALUES (?, ?, ?, ?, ?)
        ''', (key, plan, days, expiration.isoformat(), 0))
        conn.commit()

def get_key(key):
    """Obtiene una llave de Key.db."""
    with sqlite3.connect(KEY_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM keys WHERE key=?', (key,))
        result = cursor.fetchone()
    return result

def claim_key(key, user_id):
    """Registra una llave como canjeada en Claim.db."""
    with sqlite3.connect(KEY_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE keys SET claimed=1 WHERE key=?', (key,))
        conn.commit()
    
    with sqlite3.connect(CLAIM_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS claims (
                key TEXT PRIMARY KEY,
                user_id INTEGER,
                claimed_at DATETIME
            )
        ''')
        cursor.execute('''
            INSERT OR REPLACE INTO claims (key, user_id, claimed_at)
            VALUES (?, ?, ?)
        ''', (key, user_id, datetime.now().isoformat()))
        conn.commit()

def update_viped(user_id, days):
    """Actualiza los días en Viped.txt."""
    with open("Viped.txt", "a") as file:
        file.write(f"{user_id},{days}\n")

def log_error(message):
    """Guarda un mensaje de error en errors.db."""
    with sqlite3.connect(ERROR_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            INSERT INTO errors (message)
            VALUES (?)
        ''', (message,))
        conn.commit()
