import logging
from pyrogram import Client, filters
import config
import importlib
import os
import sqlite3
from datetime import datetime
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram").setLevel(logging.INFO)

app = Client("my_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

def create_tables():
    try:
        conn = sqlite3.connect('/storage/emulated/0/Download/Natsumichkbot/Natsumi.db')
        cursor = conn.cursor()

        # Crear tabla de usuarios registrados con columnas en el orden deseado
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registered_users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                rango TEXT DEFAULT 'Free User',
                poder TEXT DEFAULT 'None',
                dias INTEGER DEFAULT 0,
                creditos INTEGER DEFAULT 0,
                antispam INTEGER DEFAULT 40,
                ban TEXT DEFAULT 'False',
                razon TEXT,
                registration_date TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error al crear las tablas: {e}")

def load_commands(app):
    commands_dir = os.path.join(os.path.dirname(__file__), "commands")
    logger.info(f"Cargando comandos desde el directorio: {commands_dir}")

    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"commands.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "setup"):
                    module.setup(app)
                    logger.info(f"Comando cargado: {module_name}")
                else:
                    logger.warning(f"No se encontró la función setup en {module_name}")
            except Exception as e:
                logger.error(f"Error al cargar el módulo {module_name}: {e}")

def is_user_registered(user_id):
    try:
        conn = sqlite3.connect('/storage/emulated/0/Download/Natsumichkbot/Natsumi.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM registered_users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        logger.error(f"Error al verificar el registro del usuario: {e}")
        return False

def is_banned(user_id):
    try:
        conn = sqlite3.connect('/storage/emulated/0/Download/Natsumichkbot/Natsumi.db')
        cursor = conn.cursor()
        cursor.execute('SELECT ban FROM registered_users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0] == 'True'  # Retorna True si el valor es 'True'
        return False
    except Exception as e:
        logger.error(f"Error al verificar el baneo del usuario: {e}")
        return False

def is_command_message(message):
    commands = ["me", "id", "cmds", "gen", "genmass", "start", "bin", "panel", "vip", "claim", "fake"]

    if message.text:
        text = message.text.strip()
        commands_pattern = "|".join(re.escape(command) for command in commands)
        pattern = re.compile(r'^[' + re.escape(' /!@#$%^&*()_+-=[]{};:\'",.<>/?|`~') + r'](' + commands_pattern + r')\b', re.IGNORECASE)
        if pattern.match(text):
            return True

    return False

@app.on_message(filters.command(["register", ".register"]))
def register_command(client, message):
    try:
        user_id = message.from_user.id
        if is_user_registered(user_id):
            message.reply("**⛧ Ya estás registrado en el bot. Puedes usar todos los comandos**")
            return

        conn = sqlite3.connect('/storage/emulated/0/Download/Natsumichkbot/Natsumi.db')
        cursor = conn.cursor()
        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO registered_users (
                id, username, rango, poder, dias, creditos, antispam, ban, razon, registration_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, message.from_user.username, 'Free User', 'None', 0, 0, 40, 'False', 'Sin razón', registration_date))
        conn.commit()
        conn.close()

        message.reply("**⛧ Te Has Registrado Exitosamente. Ahora Puedes Usar Todos Los Comandos**")
    except Exception as e:
        logger.error(f"Error al registrar el usuario: {e}")

@app.on_message(filters.create(lambda _, __, message: not is_user_registered(message.from_user.id) and is_command_message(message)))
def handle_unregistered_user(client, message):
    message.reply("**⛧ Debes registrarte con el comando /register o .register para usar los comandos**")

@app.on_message(filters.create(lambda _, __, message: is_banned(message.from_user.id) and is_command_message(message)))
def handle_banned_user(client, message):
    try:
        conn = sqlite3.connect('/storage/emulated/0/Download/Natsumichkbot/Natsumi.db')
        cursor = conn.cursor()
        cursor.execute('SELECT razon FROM registered_users WHERE id = ?', (message.from_user.id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            reason = result[0]
            message.reply(f"**Usuario Baneado** ⚠️\n**Razón**: **{reason}**")
    except Exception as e:
        logger.error(f"Error al manejar el baneo del usuario: {e}")

if __name__ == "__main__":
    create_tables()
    load_commands(app)
    app.run()