import logging
from pyrogram import Client, filters
import sqlite3

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def has_permission(user_id):
    conn = sqlite3.connect('/storage/emulated/0/Download/Natsumichkbot/Natsumi.db')
    cursor = conn.cursor()
    cursor.execute('SELECT poder FROM registered_users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0] in ['Owner', 'Seller', 'Admin']
    return False

def is_user_banned(user_id):
    conn = sqlite3.connect('/storage/emulated/0/Download/Natsumichkbot/Natsumi.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ban FROM registered_users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] == 'True' if result else False

def update_user_ban_status(user_id, ban_status, reason=None):
    try:
        conn = sqlite3.connect('/storage/emulated/0/Download/Natsumichkbot/Natsumi.db')
        cursor = conn.cursor()
        if reason:
            cursor.execute('UPDATE registered_users SET ban = ?, razon = ? WHERE id = ?', (ban_status, reason, user_id))
        else:
            cursor.execute('UPDATE registered_users SET ban = ? WHERE id = ?', (ban_status, user_id))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error al actualizar el estado de baneo del usuario: {e}")

def setup(app: Client):
    command_prefixes = ["/", ".", "?", "!", "~", "-", "@", "#", "€", "_", "&", "+", "(", ")", "*", "©", ":", ";", "`", "|", "•", "√", "π", "÷", "×", "%", "§", "∆", "£", "¥", "$", "¢", "^", "°", "=", "{", "}"]

    @app.on_message(filters.command("ban", prefixes=command_prefixes))
    def ban_command(client, message):
        if not has_permission(message.from_user.id):
            message.reply(f"[⽷](tg://user?id={message.from_user.id}) **Lo Siento No Estas Autorizado para usar este comando** ❌")
            return

        try:
            args = message.text.split(maxsplit=2)
            if len(args) < 3:
                message.reply(f"[⽷](tg://user?id={message.from_user.id}) **ID Invalida Proporciona Una ID Valida**")
                return

            user_id = int(args[1])
            reason = args[2]

            if is_user_banned(user_id):
                message.reply(f"[⽷](tg://user?id={user_id}) **Usuario** [<code>{user_id}</code>] **Ya está baneado** ❌")
                return

            update_user_ban_status(user_id, 'True', reason)

            message.reply(f"[⽷](tg://user?id={user_id}) **Usuario** [<code>{user_id}</code>] **ha sido Baneado Razón**: [<code>**{reason}**</code>]")
        except Exception as e:
            logger.error(f"**Error al banear al usuario**: {e}")
            message.reply(f"[⽷](tg://user?id={message.from_user.id}) **Error al procesar el baneo**")

    @app.on_message(filters.command("unban", prefixes=command_prefixes))
    def unban_command(client, message):
        if not has_permission(message.from_user.id):
            message.reply(f"[⽷](tg://user?id={message.from_user.id}) **Lo Siento No Estas Autorizado para usar este comando** ❌")
            return

        try:
            args = message.text.split(maxsplit=1)
            if len(args) < 2:
                message.reply(f"[⽷](tg://user?id={message.from_user.id}) **ID Invalida Proporciona Una ID Valida**")
                return

            user_id = int(args[1])

            update_user_ban_status(user_id, 'False')

            message.reply(f"[⽷](tg://user?id={user_id}) **Usuario** [<code>{user_id}</code>] **ha sido desbaneado**")
        except Exception as e:
            logger.error(f"Error al desbanear al usuario: {e}")
            message.reply(f"[⽷](tg://user?id={message.from_user.id}) **Error al procesar el desbaneo**")

    @app.on_message(filters.create(lambda _, __, message: is_user_banned(message.from_user.id)))
    def handle_banned_user(client, message):
        message.reply(f"[⽷](tg://user?id={message.from_user.id}) **Estás baneado y no puedes usar el bot**")