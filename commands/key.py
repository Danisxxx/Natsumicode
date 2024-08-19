from pyrogram import Client, filters
import random
import string
import re
import os

# Ruta de los archivos
seller_file_path = "/storage/emulated/0/Download/Natsumichkbot/commands/Seller.txt"
key_db_path = "/storage/emulated/0/Download/Natsumichkbot/Key.db"
viped_file_path = "/storage/emulated/0/Download/Natsumichkbot/commands/Viped.txt"

# Función para leer IDs de Sellers autorizados
def read_seller_ids():
    if not os.path.exists(seller_file_path):
        return []
    with open(seller_file_path, 'r') as file:
        # Extraer solo la primera parte (ID) de cada línea y manejar líneas vacías
        return [line.split()[0] for line in file if line.strip()]

# Función para generar una clave VIP
def generate_vip_key():
    return "KeyNatsumi-VIP" + ''.join(random.choices(string.ascii_letters + string.digits, k=7))

# Función para guardar una clave en Key.db
def save_key(key, days):
    with open(key_db_path, 'a') as file:
        file.write(f"key {key} {days} Días\n")

# Función para manejar el comando /key o .key
def handle_key_command(command, user_id, username):
    # Verificar si el usuario está autorizado
    if str(user_id) not in read_seller_ids():
        return "**No Tienes Permiso Para Ejecutar Este Comando**"

    # Validar y parsear el comando
    match = re.match(r'[./]key (\d+)(?: (\d+))?', command)
    if not match:
        return "**Para usar este comando Usa /Key Dias Cantidad**"

    days = int(match.group(1))
    num_keys = int(match.group(2)) if match.group(2) else 1

    response = "[[⽷]](t.me/Natsumichkbot) **Key Generada**\n" + \
               "[- - - - - - - - - - - - - - - - - - - - - - - - - -](t.me/Natsumichkbot)\n"

    for _ in range(num_keys):
        key = generate_vip_key()
        save_key(key, days)
        response += f"[[⽷]](t.me/Natsumichkbot) **Key** ➜ <code>{key}</code>\n"

    response += "[- - - - - - - - - - - - - - - - - - - - - - - - - -](t.me/Natsumichkbot)\n" + \
                f"[[⽷]](t.me/Natsumichkbot) **Dias** ➜ <code>{days}</code>\n" + \
                f"[[⽷]](t.me/Natsumichkbot) **Plan** ➜ <code>VIP</code>\n" + \
                f"[[⽷]](t.me/Natsumichkbot) **Cantidad** ➜ <code>{num_keys}</code>\n" + \
                f"[[⽷]](t.me/Natsumichkbot) **Generate By** ➜ @{username}\n" + \
                "[- - - - - - - - - - - - - - - - - - - - - - - - - -](t.me/Natsumichkbot)\n"

    return response.strip()

def setup(app):
    @app.on_message(filters.command(["key", ".key"]) & (filters.private | filters.group))
    def key_command_handler(client, message):
        user_id = message.from_user.id
        username = message.from_user.username if message.from_user.username else "Unknown"
        command = message.text.strip()

        response = handle_key_command(command, user_id, username)
        message.reply_text(response)
