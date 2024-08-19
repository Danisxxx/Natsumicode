from pyrogram import Client, filters
from pyrogram.types import Message

def setup(app: Client):
    @app.on_message(filters.command(["seller", "Seller"], prefixes=list("`~!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?") + [" "]))
    async def show_seller_list(client: Client, message: Message):
        seller_list = """
[⻨](t.me/Natsumichkbot) **Lista De Sellers**
[- - - - - - - - - - - - - - - - - - - - - - - -](t.me/Natsumichkbot)
[⻨](t.me/Natsumichkbot) Owner¹ ➜ @Sunblack12 [<code>7202754124</code>]
[⻨](t.me/Natsumichkbot) Owner² ➜ @MasterBinn3r [<code>6364510923</code>]
[⻨](t.me/Natsumichkbot) Co-Owner ➜ @geovvanycop [<code>6912324978</code>]
[⻨](t.me/Natsumichkbot) Seller¹ ➜ @Raul152526 [<code>2071364924</code>] 
[- - - - - - - - - - - - - - - - - - - - - - - -](t.me/Natsumichkbot)
                """
        await message.reply(seller_list)