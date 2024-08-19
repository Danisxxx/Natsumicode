from pyrogram import Client, filters
import re
import os
from datetime import datetime, timedelta
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)

# Rutas de los archivos
key_db_path = "/storage/emulated/0/Download/Natsumichkbot/Key.db"
viped_file_path = "/storage/emulated/0/Download/Natsumichkbot/commands/Viped.txt"

# Función para leer y actualizar Key.db y Viped.txt
def claim_key(user_id, username, key):
    if not os.path.exists(key_db_path):
        return False, "🜲 **Security LuxCheker** 🜲\n\n🜲 **No se encontró el archivo Key.db.**"

    found = False
    days = 0
    updated_lines = []

    try:
        # Leer el archivo Key.db
        with open(key_db_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if key in line and "Canjeada" not in line:
                found = True
                parts = line.strip().split()
                try:
                    days = int(parts[-2])
                except (ValueError, IndexError):
                    return False, "🜲 **Security LuxCheker** 🜲\n\n🜲 **Error en el formato de la clave.**"

                updated_lines.append(f"{key} Canjeada {days} Días\n")
            else:
                updated_lines.append(line)

        if not found:
            return False, (
                "🜲 **Security LuxCheker** 🜲\n\n"
                "🜲 **La Key Es Invalida** ❌\n"
                "🜲 **Razón**\n"
                "🜲 **La Key Ya Fue Canjeada** ❌\n"
                "🜲 **La Key Es Invalida** ❌"
            )

        # Escribir las líneas actualizadas en Key.db
        with open(key_db_path, 'w') as file:
            file.writelines(updated_lines)

        # Actualizar Viped.txt
        viped_data = {}
        if os.path.exists(viped_file_path):
            with open(viped_file_path, 'r') as file:
                for line in file:
                    parts = line.split()
                    uid = parts[0]
                    viped_data[uid] = {
                        'days': int(parts[1]) if len(parts) > 1 else 0,
                        'credits': int(parts[2]) if len(parts) > 2 else 0,
                        'expiration': parts[3] if len(parts) > 3 else '',
                        'range': parts[4] if len(parts) > 4 else 'VIP'
                    }

        expiration_date = datetime.now() + timedelta(days=days)
        viped_data[user_id] = viped_data.get(user_id, {
            'days': 0,
            'credits': 0,
            'expiration': expiration_date.strftime("%Y-%m-%d %H:%M:%S"),
            'range': 'VIP'
        })

        # Actualizar los días y la expiración
        viped_data[user_id]['days'] += days
        expiration_datetime = datetime.now() + timedelta(days=viped_data[user_id]['days'])
        expiration_timedelta = expiration_datetime - datetime.now()
        expiration_str = f"{expiration_timedelta.days}d-{expiration_timedelta.seconds//3600}h-{(expiration_timedelta.seconds//60)%60}m-{expiration_timedelta.seconds%60}s"
        viped_data[user_id]['expiration'] = expiration_str

        with open(viped_file_path, 'w') as file:
            for uid, data in viped_data.items():
                file.write(f"{uid} {data['days']} {data['credits']} {data['expiration']} {data['range']}\n")

        message = (
            f"🜲 **Security LuxCheker** 🜲\n\n"
            f"🜲 **Key <code>{key}</code> Canjeada Exitosamente**\n"
            f"🜲 **Key Activa** ✅\n"
            f"🜲 **Días**: **{days}**\n"
            f"🜲 **Expiración**: **{viped_data[user_id]['expiration']}**\n"
            f"🜲 **Canjeada Por**: @{username if username else 'Unknown'}"
        )

        return True, message
    except Exception as e:
        logging.error(f"Error en claim_key: {e}")
        return False, "🜲 **Security LuxCheker** 🜲\n\n🜲 **Error inesperado. Por favor, inténtalo de nuevo.**"

# Función para manejar el comando /claim o cualquier otro prefijo
def handle_claim_command(user_id, username, command):
    match = re.match(r'^[./\-+&]?claim (.+)', command, re.IGNORECASE)
    if not match:
        return (
            "🜲 **Security LuxCheker** 🜲\n\n"
            "🜲 **Uso Correcto /Claim [Key]**\n"
            "🜲 **Cualquier Usuario**"
        )

    key = match.group(1)
    success, message = claim_key(user_id, username, key)
    return message

def setup(app):
    @app.on_message(filters.command(["claim"], prefixes=["/", ".", "-", "+", "&"]) & (filters.private | filters.group))
    def claim_command_handler(client, message):
        user_id = str(message.from_user.id)
        username = message.from_user.username
        command = message.text.strip()
        response = handle_claim_command(user_id, username, command)
        message.reply_text(response)