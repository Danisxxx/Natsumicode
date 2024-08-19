from pyrogram import Client, filters
import sqlite3
import os

# Rutas de los archivos
SELLER_FILE = '/storage/emulated/0/Download/Natsumichkbot/commands/Seller.txt'
USERS_DB = '/storage/emulated/0/Download/Natsumichkbot/users.db'

def get_allowed_ids():
    allowed_ids = set()
    with open(SELLER_FILE, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts and parts[0].isdigit():
                allowed_ids.add(parts[0])
    return allowed_ids

def get_user_ids():
    conn = sqlite3.connect(USERS_DB)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM registered_users')  # Asegúrate de que la tabla sea 'registered_users'
    user_ids = {str(row[0]) for row in cursor.fetchall()}
    conn.close()
    return user_ids

class MessageSender:
    def __init__(self, client):
        self.client = client

    async def handle_send(self, message):
        user_id = str(message.from_user.id)
        allowed_ids = get_allowed_ids()
        
        if user_id not in allowed_ids:
            await message.reply("No tienes permiso para usar este comando.")
            return
        
        user_ids = get_user_ids()

        if message.reply_to_message:
            media_message = message.reply_to_message
            if media_message:
                for uid in user_ids:
                    try:
                        # Reenviar el mensaje
                        await self.client.forward_messages(chat_id=uid, from_chat_id=media_message.chat.id, message_ids=[media_message.message_id])
                    except Exception as e:
                        print(f"Error reenviando mensaje a {uid}: {e}")
                await message.reply("Mensaje reenviado a todos los usuarios.")
        elif len(message.command) > 1:
            message_text = ' '.join(message.command[1:])
            for uid in user_ids:
                try:
                    await self.client.send_message(chat_id=uid, text=message_text)
                except Exception as e:
                    print(f"Error enviando mensaje a {uid}: {e}")
            await message.reply("Mensaje enviado a todos los usuarios.")
        else:
            await message.reply("Por favor, proporciona un mensaje o responde a un mensaje para reenviar.")

def setup(app: Client):
    message_sender = MessageSender(app)

    @app.on_message(filters.command("enviar") | filters.command(".enviar"))
    async def enviar(client, message):
        await message_sender.handle_send(message)

