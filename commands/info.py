import os
import sqlite3
from pyrogram import Client, filters as PyrogramFilters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re
from datetime import datetime, timedelta
import traceback

VIPED_FILE = "/storage/emulated/0/Download/Natsumichkbot/commands/Viped.txt"
BANS_DB_PATH = '/storage/emulated/0/Download/Natsumichkbot/baneados.db'
OWNER_USERNAME = "@Sunblack12"
GROUP_LINK = "tg://user?id="

def load_viped():
    """Carga los datos de usuarios VIP desde el archivo."""
    if not os.path.exists(VIPED_FILE):
        return {}
    viped = {}
    with open(VIPED_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 5:  # Incluye rango y expiración
                user_id, days, credits, expiration, rank = parts
            elif len(parts) == 4:
                user_id, days, credits, rank = parts
                expiration = format_expiration(calculate_expiration(int(days)))
            else:
                continue
            viped[user_id] = {'days': int(days), 'credits': int(credits), 'rank': rank, 'expiration': expiration}
    return viped

def load_bans():
    """Carga los IDs baneados desde la base de datos."""
    banned_users = set()
    ensure_bans_table_exists()
    if os.path.exists(BANS_DB_PATH):
        conn = sqlite3.connect(BANS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM bans')
        rows = cursor.fetchall()
        for row in rows:
            banned_user_id = str(row[0]).strip()  # Asegúrate de que el ID esté en formato de cadena y sin espacios
            banned_users.add(banned_user_id)
        conn.close()
    return banned_users

def calculate_expiration(days):
    """Calcula el tiempo de expiración basado en los días."""
    expiration_time = datetime.now() + timedelta(days=days)
    return expiration_time

def format_expiration(expiration_time):
    """Formatea el tiempo restante hasta la expiración."""
    remaining = expiration_time - datetime.now()
    days, seconds = remaining.days, remaining.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{days}d-{hours}h-{minutes}m"

def ensure_bans_table_exists():
    """Asegura que la tabla bans existe en la base de datos."""
    conn = sqlite3.connect(BANS_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bans (
            user_id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

async def me(client: Client, message):
    try:
        # Obtén el ID de usuario y el nombre de usuario
        if message.reply_to_message:
            user_id = str(message.reply_to_message.from_user.id)
            username = message.reply_to_message.from_user.username if message.reply_to_message.from_user.username else "Sin usuario"
            full_name = message.reply_to_message.from_user.first_name
        else:
            command_text = message.text.strip()
            match = re.match(r'^[^\w\s]*\s*info\s*(@\w+|\d+)?$', command_text, re.IGNORECASE)
            if match:
                user_info = match.group(1)
                if user_info:
                    if user_info.startswith('@'):
                        user = await client.get_users(user_info)
                        user_id = str(user.id)
                        username = user.username if user.username else "Sin usuario"
                        full_name = user.first_name
                    elif user_info.isdigit():
                        user_id = user_info
                        user = await client.get_users(int(user_id))
                        username = user.username if user.username else "Sin usuario"
                        full_name = user.first_name
                else:
                    user_id = str(message.from_user.id)
                    username = message.from_user.username if message.from_user.username else "Sin usuario"
                    full_name = message.from_user.first_name
            else:
                return

        # Cargar los datos de VIP y baneados
        viped = load_viped()
        banned_users = load_bans()

        # Verifica si el usuario está baneado
        ban_status = "True" if user_id in banned_users else "False"

        # Crear la respuesta
        response = (
          f"[⾦]({GROUP_LINK}) 𝗨𝘀𝗲𝗿 𝗗𝗮𝘁𝗮 | 𝗡𝗮𝘁𝘀𝘂𝗺𝗶 𝗖𝗵𝗸\n"
            f"[- - - - - - - - - - - - - - - - - - -](t.me/Natsumichkbot)\n"
            f"[⾦]({GROUP_LINK}) **UserID**: <code>{user_id}</code>\n"
            f"[⾦]({GROUP_LINK}) **Name**: <code>{full_name}</code> <code>[{viped.get(user_id, {}).get('rank', 'Free User')}]</code>\n"
            f"[⾦]({GROUP_LINK}) **Status**: <code>{viped.get(user_id, {}).get('days', '0')}d {viped.get(user_id, {}).get('expiration', 'No Plan Contrated')}</code>\n"
            f"[⾦]({GROUP_LINK}) **Credits**: <code>{viped.get(user_id, {}).get('credits', '0')}</code>\n"
            f"[⾦]({GROUP_LINK}) **AntiSpam**: <code>30s</code>\n"
            f"[⾦]({GROUP_LINK}) **UserName**: @{username}\n"
            f"[⾦]({GROUP_LINK}) **Warnings**: 0 | [ꕤ]({GROUP_LINK}) **Banned**: <code>{ban_status}</code>\n"
            f"[- - - - - - - - - - - - - - - - - - -](t.me/Natsumichkbot)\n"
        )

        # Crear el botón con un menú emergente
        button = InlineKeyboardButton(text="𝗕𝘂𝘆 𝗡𝗮𝘁𝘀𝘂𝗺𝗶👑", url=f"https://t.me/{OWNER_USERNAME[1:]}")
        reply_markup = InlineKeyboardMarkup([[button]])

        # Enviar el mensaje con cita si hay un mensaje al que citar
        if message.reply_to_message:
            await message.reply_to_message.reply_text(response, reply_markup=reply_markup, quote=True)
        else:
            await message.reply_text(response, reply_markup=reply_markup, quote=True)

    except Exception as e:
        log_error(f"Exception: {str(e)}\nTraceback: {traceback.format_exc()}")

def log_error(error_message):
    """Registra errores en la base de datos."""
    db_path = '/storage/emulated/0/Download/Natsumichkbot/commands/Usuarios/errors.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('INSERT INTO errors (error_message) VALUES (?)', (error_message,))
    conn.commit()
    conn.close()

def setup(app: Client):
    app.add_handler(PyrogramFilters.text & PyrogramFilters.regex(r'^[^\w\s]*\s*me\s*(@\w+|\d+)?$', re.IGNORECASE), me)
