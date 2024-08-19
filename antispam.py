from datetime import datetime, timedelta
import os
from Plugins.Func import connect_to_db


# Obtenemos el directorio actual del script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Creamos un diccionario para llevar un registro de los usuarios que han usado el comando y el momento en que lo usaron por última vez.
users_last_command = {}


def antispam(user_id, command2, message):
    now = datetime.now()
    username = message.from_user.username
    chat_id = message.chat.id
    conn = connect_to_db()
    cursor = conn.cursor()
    user_id = message.from_user.id
    # Obtiene el estado del usuario desde la tabla "users"
    cursor.execute('SELECT rango FROM users WHERE user_id = ?', (user_id,))
    user_status = cursor.fetchone()

    if user_status:
        user_status = user_status[0]
    else:
        user_status = "No registrado"

    if "Owner" in user_status or "Seller" in user_status:
        antispam_duration = 0
    elif "Premium" in user_status:
        antispam_duration = 30
    else:
        antispam_duration = 90

    last_command_time = users_last_command.get(user_id, {}).get(command2)
    if last_command_time:
        time_since_last_command = now - last_command_time
        if time_since_last_command < timedelta(seconds=antispam_duration):
            time_remaining = antispam_duration - time_since_last_command.seconds
            return f"""
↯ [ Where so Fast?⚠️ ] ↯
━━━━━━━━━━━━━━
Test again in {time_remaining} seconds."""

    users_last_command.setdefault(user_id, {})[command2] = now
    return None
