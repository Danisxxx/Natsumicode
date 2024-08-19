import sqlite3

db_path = '/storage/emulated/0/Download/Natsumichkbot/user.db'

def create_tables():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear tabla de usuarios registrados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registered_users (
            id INTEGER PRIMARY KEY
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
