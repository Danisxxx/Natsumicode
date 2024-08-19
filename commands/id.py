from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import os
import traceback
from datetime import datetime

def get_user_rank(user_id: int, seller_file_path: str, viped_file_path: str) -> str:
    """Obtiene el rango del usuario desde los archivos seller y viped."""
    try:
        if os.path.exists(seller_file_path):
            with open(seller_file_path, "r") as file:
                for line in file:
                    parts = line.strip().split()
                    if parts and str(user_id) == parts[0]:
                        return parts[1] if len(parts) > 1 else "Desconocido"

        if os.path.exists(viped_file_path):
            with open(viped_file_path, "r") as file:
                for line in file:
                    parts = line.strip().split()
                    if parts and str(user_id) == parts[0]:
                        return "VIP"
    except Exception as e:
        print(f"Error al acceder a los archivos de rangos: {e}")
    return "Desconocido"

def setup(app: Client):
    @app.on_message(filters.command(["id", ".id"], prefixes=["/", "."]))
    async def get_user_info(app: Client, message: Message):
        try:
            # Obtiene el usuario
            if message.reply_to_message:
                user = message.reply_to_message.from_user
            elif len(message.command) > 1:
                user_input = message.command[1]
                try:
                    if user_input.isdigit():
                        user = await app.get_users(int(user_input))
                    else:
                        user = await app.get_users(user_input)
                except Exception as e:
                    print(f"Error al obtener el usuario: {e}")
                    await message.reply(
                        "[<a href=https://t.me/Natsumichkbot>**⽷**</a>] **Uso Correcto**\n\n"
                        "[<a href=https://t.me/Natsumichkbot>**⽷**</a>] **/id 12345678**\n\n"
                        "[<a href=https://t.me/Natsumichkbot>**⽷**</a>] **El comando se puede usar deslizando un mensaje de una persona y poniéndolo o poniendo el comando y el ID o el nombre de usuario de la persona**",
                        quote=True
                    )
                    return
            else:
                user = message.from_user

            if not user:
                await message.reply("[<a href=https://t.me/Natsumichkbot>**⽷**</a>] **No se pudo obtener la información del usuario**", quote=True)
                return

            user_id = user.id
            first_name = user.first_name or ""
            last_name = user.last_name or ""
            full_name = f"{first_name} {last_name}".strip()
            profile_url = f"tg://user?id={user_id}"
            group_id = message.chat.id
            owner_profile_url = "https://t.me/Sunblack12"

            # Rutas a los archivos de rangos
            seller_file_path = "/storage/emulated/0/Download/Natsumichkbot/commands/Seller.txt"
            viped_file_path = "/storage/emulated/0/Download/Natsumichkbot/commands/Viped.txt"
            user_rank = get_user_rank(user_id, seller_file_path, viped_file_path)

            response_text = (
                f"[<a href=https://t.me/Natsumichkbot>**⽷**</a>] **ID**: `{user_id}`\n"
                f"[<a href=https://t.me/Natsumichkbot>**⽷**</a>] **Nombre**: `{full_name}`\n"
                f"[<a href=https://t.me/Natsumichkbot>**⽷**</a>] **Rango**: `{user_rank}`\n"
                f"[<a href=https://t.me/Natsumichkbot>**⽷**</a>] **Perfil**: <a href={profile_url}>Toca Aquí</a>\n"
                f"[<a href=https://t.me/Natsumichkbot>**⽷**</a>] **GroupID**: `{group_id}`"
            )

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("⽷Owner", url=owner_profile_url)]
            ])

            await message.reply(response_text, disable_web_page_preview=True, quote=True, reply_markup=keyboard)

        except Exception as e:
            log_error(f"Exception: {str(e)}\nTraceback: {traceback.format_exc()}")

def log_error(error_message):
    """Registra errores en un archivo de log."""
    log_file_path = '/storage/emulated/0/Download/Natsumichkbot/commands/Usuarios/errors.log'
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{datetime.now()} - {error_message}\n")