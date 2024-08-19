from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def setup(app):
    @app.on_message(filters.command("cmds", prefixes=["/", "."]) & filters.private)
    async def cmds_menu(client, message):
        name = message.from_user.first_name
        text = (f"● Hola, {name} Estás en el menú\n"
                "● Presionando Gates podrás ver el listado completo de gates\n"
                "● También Perfil podrás ver tu información de cuenta\n"
                "● Por último Herramientas podrás ver las herramientas disponibles")
        
        buttons = [
            [InlineKeyboardButton("Información", callback_data="informacion")],
            [InlineKeyboardButton("Referencias", callback_data="referencias")],
            [InlineKeyboardButton("Gates", callback_data="gates")],
            [InlineKeyboardButton("Herramientas", callback_data="herramientas")]
        ]
        
        await message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    @app.on_callback_query(filters.regex("informacion"))
    async def informacion_callback(client, callback_query):
        await callback_query.message.edit_text(
            "Aquí está tu información:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Atrás", callback_data="back")]])
        )

    @app.on_callback_query(filters.regex("referencias"))
    async def referencias_callback(client, callback_query):
        await callback_query.message.edit_text(
            "Aquí están las referencias:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Atrás", callback_data="back")]])
        )

    @app.on_callback_query(filters.regex("gates"))
    async def gates_callback(client, callback_query):
        await callback_query.message.edit_text(
            "Aquí está el listado de Gates:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Atrás", callback_data="back")]])
        )

    @app.on_callback_query(filters.regex("herramientas"))
    async def herramientas_callback(client, callback_query):
        await callback_query.message.edit_text(
            "Aquí están las herramientas disponibles:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Atrás", callback_data="back")]])
        )

    @app.on_callback_query(filters.regex("back"))
    async def back_callback(client, callback_query):
        name = callback_query.from_user.first_name
        text = (f"● Hola, {name} Estás en el menú\n"
                "● Presionando Gates podrás ver el listado completo de gates\n"
                "● También Perfil podrás ver tu información de cuenta\n"
                "● Por último Herramientas podrás ver las herramientas disponibles")
        
        buttons = [
            [InlineKeyboardButton("Información", callback_data="informacion")],
            [InlineKeyboardButton("Referencias", callback_data="referencias")],
            [InlineKeyboardButton("Gates", callback_data="gates")],
            [InlineKeyboardButton("Herramientas", callback_data="herramientas")]
        ]
        
        await callback_query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
