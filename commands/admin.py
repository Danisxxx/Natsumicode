from pyrogram import Client, filters

def get_allowed_ids(file_path):
    allowed_ids = set()
    try:
        with open(file_path, "r") as file:
            for line in file:
                allowed_ids.add(line.strip().split()[0])  
    except Exception as e:
        print(f"Error al acceder al archivo de IDs: {e}")
    return allowed_ids

def add_id_to_file(file_path, user_id, title):
    try:
        with open(file_path, "a") as file:
            file.write(f"{user_id} {title}\n")
    except Exception as e:
        print(f"Error al agregar ID al archivo: {e}")

def user_already_has_role(file_path, user_id):
    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith(f"{user_id} "):
                    return True
    except Exception as e:
        print(f"Error al verificar ID en el archivo: {e}")
    return False

def get_user_role(file_path, user_id):
    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith(f"{user_id} "):
                    return line.strip().split()[1]
    except Exception as e:
        print(f"Error al obtener el rol del usuario en el archivo: {e}")
    return None

def remove_id_from_file(file_path, user_id):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        with open(file_path, "w") as file:
            for line in lines:
                if not line.startswith(f"{user_id} "):
                    file.write(line)
    except Exception as e:
        print(f"Error al eliminar ID del archivo: {e}")

def setup(app: Client):
    @app.on_message(filters.command("rank", ["/", ".", "*", ":", ";", "!", "?", "@", "#", "€", "_"]))
    async def admin(client, message):
        try:
            owner_file_path = "/storage/emulated/0/Download/Natsumichkbot/commands/Owner.txt"
            seller_file_path = "/storage/emulated/0/Download/Natsumichkbot/commands/Seller.txt"

            allowed_ids = get_allowed_ids(owner_file_path)
            user_id = str(message.from_user.id)
            args = message.text.split(maxsplit=2)

            if user_id not in allowed_ids:
                return 

            if len(args) != 3 or not args[1].isdigit():
                await message.reply(
                    "[[ꕤ]](https://t.me/+sDSsqxjypIE1Yjlh) **Dar Rango**\n\n"
                    "**Uso Correcto: /rank ID<user_id> <título>Rango**\n"                   
                    "[ - - - - - - - - - - - - - - - - - - - - - - - - ](https://t.me/+sDSsqxjypIE1Yjlh)", 
                    disable_web_page_preview=True
                )
                return

            target_user_id = args[1]
            title = args[2]

            if user_already_has_role(seller_file_path, target_user_id):
                await message.reply(
                    f"[[ꕤ]](https://t.me/+sDSsqxjypIE1Yjlh) **El usuario con ID <code>{target_user_id}</code>**Ya tiene un rango asignado**\n"                    
                    "[ - - - - - - - - - - - - - - - - - - - - - - - - ](https://t.me/+sDSsqxjypIE1Yjlh)",
                    disable_web_page_preview=True
                )
                return

            add_id_to_file(seller_file_path, target_user_id, title)

            await message.reply(
                f"[[ꕤ]](https://t.me/+sDSsqxjypIE1Yjlh) **El ID <code>{target_user_id}</code>** **Ha Sido Ascendido Al Rango** **{title}**\n"              
                "[ - - - - - - - - - - - - - - - - - - - - - - - - ](https://t.me/+sDSsqxjypIE1Yjlh)",
                disable_web_page_preview=True
            )
        except Exception as e:
            await message.reply(f"Ocurrió un error: {e}")

    @app.on_message(filters.command("unrank", ["/", "."]))
    async def unadmin(client, message):
        try:
            owner_file_path = "/storage/emulated/0/Download/Natsumichkbot/commands/Owner.txt"
            seller_file_path = "/storage/emulated/0/Download/Natsumichkbot/commands/Seller.txt"

            allowed_ids = get_allowed_ids(owner_file_path)
            user_id = str(message.from_user.id)
            args = message.text.split()

            if user_id not in allowed_ids:
                return 

            if len(args) != 2 or not args[1].isdigit():
                await message.reply(
                    "[[ꕤ]](https://t.me/+sDSsqxjypIE1Yjlh) **Quitar Rango**\n\n"
                    "**Uso Correcto: /unrank ID** <user_id>\n"                   
                    "[ - - - - - - - - - - - - - - - - - - - - - - - - ](https://t.me/+sDSsqxjypIE1Yjlh)",
                    disable_web_page_preview=True
                )
                return

            target_user_id = args[1]
            user_role = get_user_role(seller_file_path, target_user_id)

            if user_role:
                remove_id_from_file(seller_file_path, target_user_id)

                await message.reply(
                    f"[[ꕤ]](https://t.me/+sDSsqxjypIE1Yjlh) **El Id <code>{target_user_id}</code>** **Ha Sido Eliminado Del Rango** **{user_role}**\n"                
                    "[ - - - - - - - - - - - - - - - - - - - - - - - - ](https://t.me/+sDSsqxjypIE1Yjlh)",
                    disable_web_page_preview=True
                )
            else:
                await message.reply(
                    f"[[ꕤ]](https://t.me/+sDSsqxjypIE1Yjlh) **El usuario con ID <code>{target_user_id}</code> no tiene un rango asignado.**\n"                    
                    "[ - - - - - - - - - - - - - - - - - - - - - - - - ](https://t.me/+sDSsqxjypIE1Yjlh)",
                    disable_web_page_preview=True
                )
        except Exception as e:
            await message.reply(f"Ocurrió un error: {e}")
