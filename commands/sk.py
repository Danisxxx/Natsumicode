import requests
import time
from pyrogram import Client, filters
from pyrogram.types import Message

async def chk(_, m: Message):
    tic = time.perf_counter()
    skkey = m.text[len('/sk '):]

    if not skkey:
        await m.reply("<b>Input:  <code>/sk sk_live_51LsxxxxxxxxxxxxxxxRcT66y</code></b>")
        return

    pos = requests.post(
        "https://api.stripe.com/v1/tokens",
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={
            'card[number]': '4543218722787334',
            'card[cvc]': '780',
            'card[exp_month]': '07',
            'card[exp_year]': '2026'
        },
        auth=(skkey, "")
    )

    toc = time.perf_counter()

    if 'Invalid API Key provided' in pos.text:
        await m.reply(f"""
DEAD Key❌
𝐊𝐞𝐲: <code>{skkey}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Invalid API Key provided

҂ 𝐂𝐡𝐞𝐤𝐞𝐝 𝐁𝐲 <code> @{m.from_user.username}[Free User]</code>
● 𝐁𝐨𝐭 𝐁𝐲 <b><a href="tg://resolve?domain=SrDavid09">𝙎𝙖𝙣𝙘𝙝𝙚𝙯</a></b>""")
    elif 'api_key_expired' in pos.text:
        await m.reply(f"""
DEAD Key❌
𝐊𝐞𝐲: <code>{skkey}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: api_key_expired

҂ 𝐂𝐡𝐞𝐤𝐞𝐝 𝐁𝐲 <code> @{m.from_user.username}[Free User]</code>
● 𝐁𝐨𝐭 𝐁𝐲 <b><a href="tg://resolve?domain=SrDavid09">𝙎𝙚𝙝𝙘𝙚𝙯</a></b>""")
    elif 'testmode_charges_only' in pos.text:
        await m.reply(f"""
DEAD Key❌
𝐊𝐞𝐲: <code>{skkey}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: testmode_charges_only

҂ 𝐂𝐡𝐞𝐤𝐞𝐝 𝐁𝐲 <code> @{m.from_user.username}[Free User]</code>
● 𝐁𝐨𝐭 𝐁𝐲 <b><a href="tg://resolve?domain=SrDavid09">𝙎𝙒𝙨𝙝𝙚𝙯</a></b>""")
    elif 'test_mode_live_card' in pos.text:
        await m.reply(f"""
DEAD Key❌
𝐊𝐞𝐲: <code>{skkey}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: test_mode_live_card

҂ 𝐂𝐡𝐞𝐤𝐞𝐝 𝐁𝐲 <code> @{m.from_user.username}[Free User]</code>
● 𝐁𝐨𝐭 𝐁𝐲 <b><a href="tg://resolve?domain=SrDavid09">𝙎𝙎𝙝𝙚𝙹𝙩𝙘𝙨</a></b>""")
    elif 'Your card was declined.' in pos.text:
        await m.reply(f"""
LIVE ✅
𝐊𝐞𝐲: <code>{skkey}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Viva ✅

҂ 𝐂𝐡𝐞𝐤𝐞𝐝 𝐁𝐲 <code> @{m.from_user.username}[Free User]</code>
● 𝐁𝐨𝐭 𝐁𝐲 <b><a href="tg://resolve?domain=SrDavid09">𝙎𝙨𝙝𝙚𝙝𝙯</a></b>
""")
    elif 'card_error' in pos.text:
        await m.reply(f"""
LIVE ✅
𝐊𝐞𝐲: <code>{skkey}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Viva ✅

҂ 𝐂𝐡𝐞𝐤𝐞𝐝 𝐁𝐲 <code> @{m.from_user.username}[Free User]</code>
● 𝐁𝐨𝐭 𝐁𝐲 <b><a href="tg://resolve?domain=SrDavid09">𝙎𝙚𝙓𝙚𝙧𝙻𝙾𝙏𝙍</a></b>""")
    else:
        await m.reply(f"""
LIVE ✅
𝐊𝐞𝐲: <code>{skkey}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Viva ✅

҂ 𝐂𝐡𝐞𝐤𝐞𝐝 𝐁𝐲 <code> @{m.from_user.username}[Free User]</code>
● 𝐁𝐨𝐭 𝐁𝐲 <b><a href="tg://resolve?domain=SrDavid09">𝙎𝙚𝙓𝙈𝙤𝙥𝙚𝙚𝙯</a></b>""")

def setup(bot):
    bot.add_handler(filters.command(["sk"], ["/", "."]), chk)
