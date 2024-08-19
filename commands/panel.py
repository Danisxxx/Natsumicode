from pyrogram import Client, filters
import logging

footer_banner1 = 'https://imgur.com/llb5G2P.jpg'
seller_file_path = '/storage/emulated/0/Download/Natsumichkbot/commands/Seller.txt'

def is_seller(user_id):
    """ Verifica si el user_id está en el archivo Seller.txt. """
    try:
        with open(seller_file_path, 'r') as file:
            sellers = file.read().splitlines()
        return any(str(user_id) == line.split()[0] for line in sellers)
    except FileNotFoundError:
        logging.warning(f"WARNING: No se encontró el archivo Seller.txt en {seller_file_path}")
        return False

def setup(client):
    """ Configura los comandos del bot. """
    @client.on_message(filters.command(["panel"], prefixes=['.', '/', '!', '?'], case_sensitive=False) & filters.text)
    async def panel_command(client, message):
        user_id = message.from_user.id

        if is_seller(user_id):
            panel_message = (
                "⾐ COMANDOS EXCLUSIVOS ⾐\n"
                "- - - - - - - - - - - - - - - - - - - - - - - - - -\n"
                "⾐ /addcr | añadir créditos\nUso: /addcr id creditos\n"
                "- - - - - - - - - - - - - - - - - - - - - - - - - -\n"
                "⾐ /removecr | remover créditos\nUso: /removecr id creditos\n"
                "- - - - - - - - - - - - - - - - - - - - - - - - - -\n"
                "⾐ /ban | banear usuario\nUso: /ban id\n"
                "- - - - - - - - - - - - - - - - - - - - - - - - - -\n"
                "⾐ /unban | desbanear\nUso: /unban id\n"
                "- - - - - - - - - - - - - - - - - - - - - - - - - -\n"
                "⾐ /buscar | información de usuario\nUso: /buscar id\n"
                "- - - - - - - - - - - - - - - - - - - - - - - - - -\n"
                "⾐ /key | Generar Key\nUso: /key dias\n"
                "- - - - - - - - - - - - - - - - - - - - - - - - - -\n"
                "⾐ /premium | Añadir premium\nUso: /premium id dias"
            )
            await message.reply(panel_message)
        else:
            await message.reply(f"<b>Access denied. ❌</b> <a href='{footer_banner1}'>&#8203;</a>")
