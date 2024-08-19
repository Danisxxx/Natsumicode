from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json
import requests
import time
import os

# Define la carpeta temporal donde se guardará la información de los mensajes generados
TEMP_DIR = '/storage/emulated/0/Download/Natsumichk/temp'
os.makedirs(TEMP_DIR, exist_ok=True)

# Configura el cliente del bot
def setup(client):
    """Configura las funciones del cliente para el bot."""
    
    @client.on_callback_query(filters.regex(r'^regen_'))
    async def regen_callback(client, callback_query):
        """Maneja el callback del botón de regeneración"""
        data = callback_query.data[len('regen_'):]
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id

        # Leer la información guardada en el archivo JSON
        try:
            with open(f'{TEMP_DIR}/gen_message_{message_id}.json', 'r') as f:
                message_data = json.load(f)
        except FileNotFoundError:
            return await callback_query.answer("Error al encontrar los datos de la generación.")

        # Regenerar las tarjetas con el mismo BIN usando la API
        ccs = regenerate_cards(message_data['bins'])

        # Generar el texto para el mensaje con tarjetas
        text = f"""
𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐨𝐫 𝐂𝐂 𝑺𝒊𝒓𝒆𝒍𝒍𝒆 [𝐂𝐇𝐊]
- - - - - - - - - - - - - - - - - - - - -
Format - ↯ <code>{message_data['bins']}xxxxxx|{message_data['mes']}|{message_data['ano']}|{message_data['ano']}</code>
- - - - - - - - - - - - - - - - - - - - -

<code>{ccs[0]}</code>
<code>{ccs[1]}</code>
<code>{ccs[2]}</code>
<code>{ccs[3]}</code>
<code>{ccs[4]}</code>
<code>{ccs[5]}</code>
<code>{ccs[6]}</code>
<code>{ccs[7]}</code>
<code>{ccs[8]}</code>
<code>{ccs[9]}</code>
- - - - - - - - - - - - - - - - - - - - -
Bin - ↯ <code>{message_data['bins']}</code> | Time - ↯ {time.perf_counter() - callback_query.message.date.timestamp():.3f}s
Info - ↯ <code>{message_data['info']}</code>
Bank - <code>{message_data['bank']}</code>
Country <code>{message_data['country']}</code> [{message_data['flag']}]
Checked by - ↯ @{message_data['username']} [VIP]
"""

        # Actualizar el mensaje con las nuevas tarjetas
        await callback_query.message.edit_text(
            text=text,
            reply_markup=generate_inline_keyboard(message_id)  # Regenera el teclado inline
        )

        await callback_query.answer("Tarjetas regeneradas.")

def regenerate_cards(bin_prefix):
    """Genera un nuevo conjunto de tarjetas usando el mismo BIN a través de la API."""
    url = "https://namso-gen.com/api/v1/card"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "bin": bin_prefix,
        "number": 10  # Número de tarjetas a generar
    }

    try:
        response = requests.post(url, headers=headers, json=params)
        response.raise_for_status()  # Lanza un error si la solicitud falla
        data = response.json()
        card_numbers = [f"{card['number']}|{card['expiry_month']}|{card['expiry_year']}|{card['cvv']}" for card in data['cards']]
        return card_numbers
    except requests.RequestException as e:
        print(f"Error al generar tarjetas: {e}")
        return ["Error al generar tarjetas"] * 10

def generate_inline_keyboard(message_id):
    """Genera el teclado inline con el botón de regeneración."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("☊ Regen ⥻", callback_data=f"regen_{message_id}")]
    ])

# Guardar la información del mensaje original en un archivo JSON
def save_message_data(message_id, bins, mes, ano, info, bank, country, flag, username):
    message_data = {
        "bins": bins,
        "mes": mes,
        "ano": ano,
        "info": info,
        "bank": bank,
        "country": country,
        "flag": flag,
        "username": username
    }
    with open(f'{TEMP_DIR}/gen_message_{message_id}.json', 'w') as f:
        json.dump(message_data, f)