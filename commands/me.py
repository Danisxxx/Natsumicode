from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3
import re

def setup(app):
    @app.on_message(filters.regex(r'(?i)^[\./!]\bme\b'))
    async def me_command(client, message):
        # Separar los componentes del mensaje
        text = message.text or ""
        command_parts = text.split()

        # Definir usuario objetivo inicial como el que ejecuta el comando
        target_user = message.from_user

        # Verificar si se respondió a un mensaje que menciona a otro usuario
        if message.reply_to_message and message.reply_to_message.from_user:
            target_user = message.reply_to_message.from_user
        # Verificar si se especificó un nombre de usuario o ID después del comando
        elif len(command_parts) > 1:
            identifier = command_parts[1]
            if identifier.startswith('@'):
                identifier = identifier[1:]  # Quitar el '@' del nombre de usuario
            if identifier.isdigit():
                # Buscar por ID
                target_user = await client.get_users(int(identifier))
            else:
                # Buscar por nombre de usuario
                target_user = await client.get_users(identifier)

        # Obtener información básica del usuario
        user_id = target_user.id
        username = target_user.username
        user_link = f"tg://user?id={user_id}"
        first_name = target_user.first_name or "N/A"

        # Conectar a la base de datos
        conn = sqlite3.connect('/storage/emulated/0/Download/Natsumichkbot/Natsumi.db')
        cursor = conn.cursor()

        # Obtener datos del usuario desde la base de datos
        cursor.execute("SELECT * FROM registered_users WHERE ID = ?", (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            # Extraer datos según el orden de las columnas
            name = user_data[1]
            rank = user_data[2]
            days = user_data[4]
            credits = user_data[5]
            anti_spam = user_data[6]
            banned = user_data[7]

            # Formatear el mensaje
            message_text = f"""
𝙉𝙖𝙩𝙨𝙪𝙢𝙞 | 𝕯𝖆𝖙𝖆 𝖀𝖘𝖊𝖗⚡
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - -](https://t.me/Natsumichkbot)
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **User** ➜ <a href="{user_link}">{first_name}</a> 
[<a href=https://t.me/Natsumichkbot>**衣**</a>] **UserID** » [<code>**{user_id}**</code>] | **Ban** [**{banned}**]
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - -](https://t.me/Natsumichkbot)
[<a href=https://t.me/Natsumichkbot>**衣**</a>] 𝙉𝙖𝙩𝙨𝙪𝙢𝙞 | 𝙈𝙚𝙢𝙗𝙚𝙧𝙨𝙝𝙞𝙥 ⚡:
[<a href=https://t.me/Natsumichkbot>**衣**</a>] **Rank** » **{rank}** | **Credits** » **{credits}**
[<a href=https://t.me/Natsumichkbot>**衣**</a>] **Antispam** » **{anti_spam}**
[<a href=https://t.me/Natsumichkbot>**衣**</a>] **Days** » **{days}**
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - -](https://t.me/Natsumichkbot)
                       """
        else:
            message_text = "User data not found."

        # Crear botones inline alineados horizontalmente
        inline_keyboard = [
            [
                InlineKeyboardButton("𝘾𝙝𝙖𝙩 𝙁𝙧𝙚𝙚 ⚠️", url="https://t.me/+8SjFYVLZPpZhNDAx"),
                InlineKeyboardButton("𝘽𝙪𝙮 𝘾𝙃𝙆 ⚡", url="https://t.me/sunblack12")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)

        # Responder al mensaje original con los botones inline
        await message.reply(message_text, quote=True, reply_markup=reply_markup)

        # Cerrar la conexión a la base de datos
        conn.close()