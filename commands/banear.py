from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid

def setup(client: Client):
    @client.on_message(filters.command("banear", prefixes=["/", "."]) & filters.group)
    def banear(client, message):
        chat_id = message.chat.id
        if len(message.command) == 2:
            arg = message.command[1]
            user_id = None

            if arg.startswith('@'):
                username = arg[1:]
                try:
                    user = client.get_users(username)
                    user_id = user.id
                except PeerIdInvalid:
                    message.reply("**[⎔](tg://user?id=)Usuario no encontrado**")
                    return
            else:
                try:
                    user_id = int(arg)
                except ValueError:
                    message.reply("**[⎔](tg://user?id=)ID no válido. Usa /banear @username**")
                    return

            if user_id:
                try:
                    client.ban_chat_member(chat_id, user_id)
                    message.reply(f"**[⎔](tg://user?id=) El Usuario Con ID <code>[{user_id}]</code> Ha Sido Baneado**")
                except PeerIdInvalid:
                    message.reply("**[⎔](tg://user?id=)No se pudo banear al usuario**")
            else:
                message.reply("**[⎔](tg://user?id=)Usuario no encontrado**")
        else:
            message.reply("**[⎔](tg://user?id=)Uso incorrecto Usa /banear @username**")

    @client.on_message(filters.command("desbanear", prefixes=["/", "."]) & filters.group)
    def desbanear(client, message):
        chat_id = message.chat.id
        if len(message.command) == 2:
            arg = message.command[1]
            user_id = None

            if arg.startswith('@'):
                username = arg[1:]
                try:
                    user = client.get_users(username)
                    user_id = user.id
                except PeerIdInvalid:
                    message.reply("**[⎔](tg://user?id=)Usuario no encontrado**")
                    return
            else:
                try:
                    user_id = int(arg)
                except ValueError:
                    message.reply("**[⎔](tg://user?id=)ID no válido. Usa /desbanear @username**")
                    return

            if user_id:
                try:
                    client.unban_chat_member(chat_id, user_id)
                    message.reply(f"[⎔](tg://user?id=) **El usuario con ID <code>[{user_id}]</code> ha sido desbaneado**")
                except PeerIdInvalid:
                    message.reply("[⎔](tg://user?id=) **No se pudo desbanear al usuario**")
            else:
                message.reply("[⎔](tg://user?id=) **Usuario no encontrado**")
        else:
            message.reply("[⎔](tg://user?id=) **Uso incorrecto. Usa /desbanear @username**")
