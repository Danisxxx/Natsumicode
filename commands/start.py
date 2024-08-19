from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def register(app: Client):
    @app.on_message(filters.command(["start", ".start"]))
    async def start(client, message):
        user_id = message.from_user.id
        
        menu_text = f"""
**𝖧𝗈𝗆𝖾** | 𝙉𝙖𝙩𝙨𝙪𝙢𝙞 ⚡
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Bienvenido [<code>**{user_id}**</code>] Al menú principal de Natsumi chk Esta es la versión 1.0 de Natsumi.
Contiene lo que contienen los botones. Tócalos y verás**
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
**Escriben /cmds Para Ver las herramientas Disponibles**
        """

        buttons = [
            [InlineKeyboardButton("Tools", callback_data="tools_intro"), InlineKeyboardButton("Gates", callback_data="gates")],
            [InlineKeyboardButton("Finish❌", callback_data="finish")]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        await message.reply_text(menu_text, reply_markup=reply_markup, quote=True)

    @app.on_callback_query()
    async def callback_private(client, callback_query):
        reply_message = callback_query.message.reply_to_message
        if reply_message is not None and reply_message.from_user is not None:
            if reply_message.from_user.id != callback_query.from_user.id:
                return await callback_query.answer("Lo Siento Usa Tu Propio Menu ⚠️", show_alert=True)
        await callback_query.continue_propagation()

    @app.on_callback_query(filters.regex("finish"))
    async def finish(client, callback_query):
        await callback_query.message.delete()

    @app.on_callback_query(filters.regex("back"))
    async def back(client, callback_query):
        user_id = callback_query.from_user.id
        
        menu_text = f"""
**𝖧𝗈𝗆𝖾** | 𝙉𝙖𝙩𝙨𝙪𝙢𝙞 ⚡
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Bienvenido [<code>**{user_id}**</code>] Al menú principal de Natsumi chk Esta es la versión 1.0 de Natsumi.
Contiene lo que contienen los botones. Tócalos y verás**
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
**Escriben /cmds Para Ver las herramientas Disponibles**
        """

        buttons = [
            [InlineKeyboardButton("Tools", callback_data="tools_intro"), InlineKeyboardButton("Gates", callback_data="gates")],
            [InlineKeyboardButton("Finish❌", callback_data="finish")]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        await callback_query.message.edit_text(menu_text, reply_markup=reply_markup)

    @app.on_callback_query(filters.regex("tools_intro"))
    async def tools_intro(client, callback_query):
        user_id = callback_query.from_user.id

        tools_intro_text = f"""
**Tools List** | 𝙉𝙖𝙩𝙨𝙪𝙢𝙞 ⚡
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Como estás** <code>**{callback_query.from_user.first_name}**</code> **Está Es Lista De Herramientas Espero Te gusten Y te sirvan
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
 [<a href="https://t.me/Natsumichkbot">**衣**</a>] **Tools** ➜ 5 ✅ [ON] 
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Toca Estos Botones Para ver las herramientas Disponibles**

        """
        buttons = [
            [InlineKeyboardButton("🛠️Tools", callback_data="tools_1"), InlineKeyboardButton("↺Back", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        await callback_query.message.edit_text(tools_intro_text, reply_markup=reply_markup)

    @app.on_callback_query(filters.regex("tools_1"))
    async def tools_page_1(client, callback_query):
        user_id = callback_query.from_user.id

        tools_text = f"""
Tools List | 𝙉𝙖𝙩𝙨𝙪𝙢𝙞 ⚡
**Page**: **1**
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖭𝖺𝗆𝖾**: **Generator CC Card**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖢𝗈𝗆𝗆𝖺𝗇𝖽: /gen**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Status**: **Free Users** ⚡
[<a href="https://t.me/Natsumichkbot">**衣**</a>] 𝖲𝗍𝖺𝗍𝗎𝗌: **ON [✅]**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Example**: **/gen** **123456**
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖭𝖺𝗆𝖾**: **Fake adress**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖢𝗈𝗆𝗆𝖺𝗇𝖽**: **/fake**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Status**: **Free User** ⚡
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖲𝗍𝖺𝗍𝗎𝗌**: **ON [✅]**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Example**: **/fake Mx , Ca ,Us ,Ve ,Br**
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖭𝖺𝗆𝖾**: **Bin Check Valid**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖢𝗈𝗆𝗆𝖺𝗇𝖽**: **/bin**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Status**: **Free User** ⚡
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖲𝗍𝖺𝗍𝗎𝗌**: **ON [✅]**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Example**: **/bin 123456**
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖭𝖺𝗆𝖾**: **extras generator**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖢𝗈𝗆𝗆𝖺𝗇𝖽**: **/extra**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Status**: **Free User** ⚡
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖲𝗍𝖺𝗍𝗎𝗌**: **OFF [✖️]**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Example**: **/extra**
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
        """
        buttons = [
            [InlineKeyboardButton("↺ Back", callback_data="tools_intro"), InlineKeyboardButton("Next ↻", callback_data="tools_2")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        await callback_query.message.edit_text(tools_text, reply_markup=reply_markup)

    @app.on_callback_query(filters.regex("tools_2"))
    async def tools_page_2(client, callback_query):
        tools_text = f"""
Tools List | 𝙉𝙖𝙩𝙨𝙪𝙢𝙞 ⚡
**Page** : **2**
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖭𝖺𝗆𝖾**: **Send References**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖢𝗈𝗆𝗆𝖺𝗇𝖽**: **/Refes**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Status**: **Seller** ⚡
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖲𝗍𝖺𝗍𝗎𝗌**: **OFF** **[✖]**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Example**: **/Refes Desliza una imagen**
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖭𝖺𝗆𝖾**: **Check 3d**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖢𝗈𝗆𝗆𝖺𝗇𝖽**: **/vbv**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Status**: **VIP** ⚡
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **𝖲𝗍𝖺𝗍𝗎𝗌**: ON [✅]
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Example**: **/vbv 1234567|12|29|000**
[- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
        """
        buttons = [
            [InlineKeyboardButton("↺ Back", callback_data="tools_1")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        await callback_query.message.edit_text(tools_text, reply_markup=reply_markup)

def setup(app: Client):
    register(app)