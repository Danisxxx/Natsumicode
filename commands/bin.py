import requests
from pyrogram import Client, filters
import re

def setup(client):
    @client.on_message(filters.regex(r'^[^\w\s]+[bB][iI][nN]\b') & filters.text)
    async def cmds(client, message):
        try:
            input_text = message.text.split(None, 1)
            if len(input_text) < 2:
                return await message.reply("""
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] 𝗡𝗮𝘁𝘀𝘂𝗺𝗶 𝗖𝗛𝗞 ϟ [ **BIN INFO** ] 
[- - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Bin** ➜ **No Valido** ❌
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Input** ➜ **/bin 123456** ✅
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Message** ➜ **Ingresa un bin Valido** :)
[- - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **User**: **@{}**
                """.format(message.from_user.username or 'Unknown'))

            BIN = input_text[1][:6]

            if len(BIN) != 6 or not BIN.isdigit():
                return await message.reply("""
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] 𝗡𝗮𝘁𝘀𝘂𝗺𝗶 𝗖𝗛𝗞 ϟ [ **BIN INFO** ] 
[- - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Bin** ➜ **No Valido**? ✘
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Input** ➜ **/bin 458294** ✅
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] ***Message** ➜ **Ingresa un bin Valido** :)
[- - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] User: **@{}**
                """.format(message.from_user.username or 'Unknown'))

            response = requests.get(f"https://bins.antipublic.cc/bins/{BIN}")
            req = response.json()

            if 'bin' not in req:
                await message.reply(f"""
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] 𝗡𝗮𝘁𝘀𝘂𝗺𝗶 𝗖𝗛𝗞 ϟ [ **BIN INFO** ] 
[- - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Bin** ➜ **{BIN}**
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Info** ➜ **No se encontró información**
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Bank** ➜ **No disponible**
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Country** ➜ **No disponible**
[- - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] User: **@{message.from_user.username or 'Unknown'}**
                """)
            else:
                brand = req.get('brand', 'Información no disponible')
                country_name = req.get('country_name', 'Información no disponible')
                country_flag = req.get('country_flag', '🚩')
                bank = req.get('bank', 'Información no disponible')

                await message.reply(f"""
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] 𝗡𝗮𝘁𝘀𝘂𝗺𝗶 𝗖𝗛𝗞 ϟ [ **BIN INFO** ] 
[- - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Bin** ➜ <code>**{BIN}**</code>
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Info** ➜ <code>**{brand}**</code>
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Bank** ➜ <code>**{bank}**</code>
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Country** ➜ <code>**{country_name}**</code> {country_flag}
[- - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Status** ➜ ✅ <code>**Valid Bin**</code>
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **User** ➜ **@{message.from_user.username or 'Unknown'}**
                """)
        except IndexError:
            await message.reply("""
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] 𝗡𝗮𝘁𝘀𝘂𝗺𝗶 𝗖𝗛𝗞 ϟ [ **BIN INFO** ] 
[- - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Bin** ➜ **No Valido** ?? ✘
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] ***Input** ➜ **/bin 442939** ✅
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Message** ➜ **Ingresa un bin Valido**:)
[- - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **User**: **@{message.from_user.username or 'Unknown'}**
            """)
        except ValueError:
            await message.reply("""
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] 𝗡𝗮𝘁𝘀𝘂𝗺𝗶 𝗖𝗛𝗞 ϟ [ **BIN INFO** ] 
[- - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Bin** ➜ **No Valido** ?? ✘
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Input** ➜ **/bin 448288** ✅
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **Message** ➜ **Ingresa un bin Valido**:)
[- - - - - - - - - - - - - - - - - - - - - - - -](tg://user?id=)
[<a href="https://t.me/Natsumichkbot">**⽷**</a>] **User**: **@{message.from_user.username or 'Unknown'}**
            """)

