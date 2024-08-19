import sqlite3
from pyrogram import Client

app = Client("my_bot")

@app.on_message()
async def handle_message(client, message):
    # Asegúrate de que el mensaje provenga de un usuario autorizado
    if message.text.startswith("/ban"):
        # Extrae el ID del usuario a banear del mensaje
        command_parts = message.text.split()
        if len(command_parts) < 2:
            await message.reply("**Debes proporcionar el ID del usuario a banear**)
            return

        try:
            user_id = int(command_parts[1])
            ban_user_in_db(user_id)
            await message.reply(f"**Usuario con ID {user_id} ha sido baneado**")
        except ValueError:
            await message.reply("**El ID del usuario debe ser un número entero**")
        except Exception as e:
            await message.reply(f"**Ocurrió un error**: {e}")

def ban_user_in_db(user_id):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO banned_users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run()
