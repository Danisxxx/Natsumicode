import time
import random
import re
import csv
import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

def load_country_flags(file_path):
    country_flags = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            country_flags[row['country_name'].upper()] = row['country_flag']
    return country_flags

country_flags = load_country_flags('/storage/emulated/0/Download/Natsumichkbot/commands/countries_flags.csv')

def luhn_verification(num):
    num = [int(d) for d in str(num)]
    check_digit = num.pop()
    num.reverse()
    total = 0
    for i, digit in enumerate(num):
        if i % 2 == 0:
            digit = digit * 2
        if digit > 9:
            digit = digit - 9
        total += digit
    total = total * 9
    return (total % 10) == check_digit

def cc_gen(cc, mes='x', ano='x', cvv='x'):
    ccs = []
    while len(ccs) < 10:
        card = str(cc)
        digits = '04567896789'
        list_digits = list(digits)
        random.shuffle(list_digits)
        string_digits = ''.join(list_digits)
        card = card + string_digits
        if card[0] == '3':
            card = card[0:15]
        else:
            card = card[0:16]

        if mes == 'x':
            mes_gen = random.randint(1, 12)
            if len(str(mes_gen)) == 1:
                mes_gen = '0' + str(mes_gen)
        else:
            mes_gen = mes

        if ano == 'x':
            ano_gen = random.randint(2023, 2031)
        else:
            ano_gen = ano
            if len(str(ano_gen)) == 2:
                ano_gen = '20' + str(ano_gen)

        if cvv == 'x':
            if card[0] == '3':
                cvv_gen = random.randint(1000, 9999)
            else:
                cvv_gen = random.randint(100, 999)
        else:
            cvv_gen = cvv

        x = str(card) + '|' + str(mes_gen) + '|' + str(ano_gen) + '|' + str(cvv_gen)
        if luhn_verification(card):
            ccs.append(x)
        else:
            continue

    return ccs

def get_bin_info(bin):
    try:
        response = requests.get(f"https://bins.antipublic.cc/bins/{bin}")
        if response.status_code == 200:
            data = response.json()
            bank = data.get('bank', 'Unknown')
            brand = data.get('brand', 'Unknown')
            typea = data.get('type', 'Unknown')
            country = data.get('country_name', 'Unknown').upper()

            country_flag = country_flags.get(country, '')

            return bank, brand, typea, country, country_flag
        else:
            return "Unknown", "Unknown", "Unknown", "Unknown", ""
    except Exception as e:
        print(f"Error fetching BIN info: {e}")
        return "Unknown", "Unknown", "Unknown", "Unknown", ""

def setup(client: Client):
    @client.on_message(filters.command("genmass", prefixes=['/', '.', '$', '-'], case_sensitive=False))
    async def gen(client: Client, m: Message):
        bin_pattern = re.compile(r'(\d{6})[^\d]*')
        date_pattern = re.compile(r'(\d{2})[:!/\|](\d{2,4})')

        def extract_date(text):
            match = date_pattern.search(text)
            if match:
                month, year = match.groups()
                if len(year) == 2:
                    year = '20' + year
                return month, year
            return 'x', 'x'

        def extract_bin(text):
            match = bin_pattern.search(text)
            if match:
                return match.group(1)
            return '000000'

        if m.reply_to_message:
            original_message = m.reply_to_message.text
            BIN = extract_bin(original_message)
            mes, ano = extract_date(original_message)
        else:
           
            text = m.text
            BIN = extract_bin(text)
            mes, ano = extract_date(text)

        if BIN == '000000' or not BIN:
            await m.reply_text("⚠️ **Bins Inválido** : **Proporciona un bins Válido Ejemplo /genmass 53684**")
            return

        tiempoinicio = time.perf_counter()

        ccs = cc_gen(BIN, mes, ano)

        tiempofinal = time.perf_counter()
        username = m.from_user.username if m.from_user.username else m.from_user.id

        bank, brand, typea, country, country_flag = get_bin_info(BIN)

        response = f"""<b> 𝐍𝐚𝐭𝐬𝐮𝐦𝐢 𝐆𝐞𝐧𝐦𝐚𝐬𝐬 
[- - - - - - - - - - - - - - - - - - - - - - - - -](t.me/Natsumichkbot)
Bin - ↯ <code>{BIN}</code> Time - ↯ <code>{tiempofinal - tiempoinicio:0.3f}</code>s
Input - ↯ <code>{BIN}|{mes}|{ano}</code>
[- - - - - - - - - - - - - - - - - - - - - - - - -](t.me/Natsumichkbot)
"""

        response += '\n'.join([f"<code>{cc}</code>" for cc in ccs])
        response += f"""
[- - - - - - - - - - - - - - - - - - - - - - - - -](t.me/Natsumichkbot)
[[⽷]](t.me/Natsumichkbot) Bank : <code>{bank}</code>
[[⽷]](t.me/Natsumichkbot) Data : <code>{brand}-{typea}</code>
[[⽷]](t.me/Natsumichkbot) Country : <code>{country}</code> {country_flag}
[[⽷]](t.me/Natsumichkbot) Checked by - ↯ @{username}</b>"""

        buttons = [
            [InlineKeyboardButton("ReGen", callback_data=f"regen_{username}_{BIN}_{mes}_{ano}")]
        ]

        keyboard = InlineKeyboardMarkup(buttons)
        await m.reply_text(response, reply_markup=keyboard)

    @client.on_callback_query()
    async def handle_callback_query(client: Client, callback_query: CallbackQuery):
        data = callback_query.data.split('_')
        if data[0] == 'regen':
            username = data[1]
            BIN = data[2]
            mes = data[3]
            ano = data[4]

            tiempoinicio = time.perf_counter()
            
            ccs = cc_gen(BIN, mes, ano)

            tiempofinal = time.perf_counter()

            bank, brand, typea, country, country_flag = get_bin_info(BIN)

            response = f"""<b> 𝐍𝐚𝐭𝐬𝐮𝐦𝐢 𝐆𝐞𝐧𝐦𝐚𝐬𝐬 
[- - - - - - - - - - - - - - - - - - - - - - - - -](t.me/Natsumichkbot)
Bin - ↯ <code>{BIN}</code> Time - ↯ <code>{tiempofinal - tiempoinicio:0.3f}</code>s
Input - ↯ <code>{BIN}|{mes}|{ano}</code>
[- - - - - - - - - - - - - - - - - - - - - - - - -](t.me/Natsumichkbot)
"""

            response += '\n'.join([f"<code>{cc}</code>" for cc in ccs])
            response += f"""
[- - - - - - - - - - - - - - - - - - - - - - - - -](t.me/Natsumichkbot)
[[⽷]](t.me/Natsumichkbot) Bank : <code>{bank}</code>
[[⽷]](t.me/Natsumichkbot) Data : <code>{brand}-{typea}</code>
[[⽷]](t.me/Natsumichkbot) Country : <code>{country}</code> {country_flag}
[[⽷]](t.me/Natsumichkbot) Checked by - ↯ @{username}</b>"""

            buttons = [
                [InlineKeyboardButton("ReGen", callback_data=f"regen_{username}_{BIN}_{mes}_{ano}")]
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            await callback_query.message.edit_text(response, reply_markup=keyboard)

