from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def setup(app):
    @app.on_message(filters.command(["prices", ".prices"]))
    def send_prices(client, message):
        prices_text = """𝗠𝗘𝗠𝗕𝗥𝗘𝗦𝗜‌𝗔
𝗩𝗜𝗣
𝟳 𝗗𝗜𝗔𝗦 = 1 𝗨𝗦𝗗
𝟭𝟱 𝗗𝗜𝗔𝗦 = 3 𝗨𝗦𝗗
𝟯𝟬 𝗗𝗜𝗔𝗦 = 5 𝗨𝗦𝗗

𝗠𝗘𝗧𝗢𝗗𝗢𝗦 𝗗𝗘 𝗣𝗔𝗚𝗢

- 𝗣𝗔𝗬𝗣𝗔𝗟 
- 𝗕𝗜𝗡𝗔𝗡𝗖𝗘"""
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🜲Owner", url="https://t.me/Daniels_1906")],
            [InlineKeyboardButton("🜲Seller", url="https://t.me/c/2169525971/26")]
        ])
        
        message.reply_text(prices_text, reply_markup=keyboard, quote=True)
