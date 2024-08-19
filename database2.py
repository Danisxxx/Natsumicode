import sqlite3

db_path = '/storage/emulated/0/Download/Natsumichkbot/user.db'

def create_table():
    """Crea la tabla de usuarios registrados si no existe."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registered_users (
            id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

def is_user_registered(user_id):
    """Verifica si un usuario está registrado."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM registered_users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def register_user(user_id):
    """Registra un nuevo usuario."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Verificar si el usuario ya está registrado
    if is_user_registered(user_id):
        conn.close()
        return False  # Usuario ya registrado

    # Registrar al usuario
    cursor.execute('INSERT INTO registered_users (id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()
    return True  # Registro exitoso

# Asegurarse de que la tabla existe
create_table()
