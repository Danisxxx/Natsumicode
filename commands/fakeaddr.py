import sqlite3
import requests
import csv
from pyrogram import Client, filters

# Cargar banderas de países desde el archivo CSV
def load_country_flags(filename):
    country_flags = {}
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                country_flags[row['country_code'].upper()] = row['country_flag']
    except FileNotFoundError:
        print(f"Archivo {filename} no encontrado.")
    except Exception as e:
        print(f"Error al cargar banderas: {e}")
    return country_flags

# Cargar el diccionario de banderas
country_flags = load_country_flags('/storage/emulated/0/Download/Natsumichkbot/commands/countries_flags.csv')

def get_random_address(country_code):
    url = f'https://randomuser.me/api/?nat={country_code}'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error en la solicitud de dirección: {e}")
        return None

    data = response.json()
    if not data.get('results'):
        return None

    result = data['results'][0]
    location = result.get('location', {})

    # Extraer y formatear los datos de la dirección
    street_data = location.get('street', {})
    street = f"{street_data.get('number', '')} {street_data.get('name', '')}"

    address = {
        'name': f"{result['name']['first']} {result['name']['last']}",
        'street': street,
        'city': location.get('city', 'N/A'),
        'state': location.get('state', 'N/A'),
        'postal_code': location.get('postcode', 'N/A'),
        'phone': result.get('phone', 'N/A'),
        'country': location.get('country', 'N/A'),
        'flag': country_flags.get(country_code.upper(), '🏳️')  # Usa la bandera del diccionario o un marcador de posición
    }
    return address

def get_temp_email():
    try:
        response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1')
        response.raise_for_status()
        return response.json()[0]
    except requests.RequestException as e:
        print(f"Error al obtener el correo temporal: {e}")
        return None

def get_user_rank(user_id):
    conn = sqlite3.connect('/storage/emulated/0/Download/Natsumichkbot/Natsumi.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT rango FROM registered_users WHERE ID = ?", (user_id,))
        result = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error al consultar la base de datos: {e}")
        result = None
    
    conn.close()
    
    return result[0] if result else 'Usuario'  # Si no encuentra rango, muestra "Usuario" por defecto

def setup(app):
    @app.on_message(filters.command(['fake', '.fake']))
    async def fake_address(client, message):
        command = message.text.split()
        if len(command) != 2:
            await message.reply(f" [<a href=https://t.me/Natsumichkbot>**衣**</a>] 𝗡𝗮𝘁𝘀𝘂𝗺𝗶 𝗖𝗛𝗞 ϟ [ **RAND ADDRESS** ]\n"
             "[- - - - - - - - - - - - - - - - - - - - - - - -](https://t.me/Natsumichkbot)\n"
            "[<a href=https://t.me/Natsumichkbot>**衣**</a>] **Address ➜ No Válido** ❌\n"
            "[<a href=https://t.me/Natsumichkbot>**衣**</a>] **Input ➜ /fake MX** ✅\n"
            "[<a href=https://t.me/Natsumichkbot>**衣**</a>] **Access** ➜ Free User**\n"
            "[- - - - - - - - - - - - - - - - - - - - - - - -](https://t.me/Natsumichkbot)\n"
            )
            return

        country_code = command[1]
        address = get_random_address(country_code)
        email = get_temp_email()

        if not address or not email:
            await message.reply("Código de país no soportado o error en la generación de la dirección o correo.")
            return

        user_id = message.from_user.id
        rank = get_user_rank(user_id)
        tg_link = f"tg://user?id={user_id}"

        response = f"""
𝗡𝗮𝘁𝘀𝘂𝗺𝗶 𝗖𝗛𝗞 ϟ [ **RAND ADDRESS** ]
[- - - - - - - - - - - - - - - - - - - - - - - -](https://t.me/Natsumichkbot)
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Name** ➜ <code>{address['name']}</code>
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Street** ➜ <code>{address['street']}</code>
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **State** ➜ <code>{address['state']}</code>
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **City** ➜ <code>{address['city']}</code>
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Zip** ➜ <code>{address['postal_code']}</code>
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Phone** ➜ <code>{address['phone']}</code>
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Country** ➜ <code>{address['country']}</code> {address['flag']}
[- - - - - - - - - - - - - - - - - - - - - - - -](https://t.me/Natsumichkbot)
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **Status** ➜ ✅ **Valid Street**
[<a href="https://t.me/Natsumichkbot">**衣**</a>] **User** ➜ <a href="{tg_link}">{message.from_user.first_name}</a> **[{rank}]**
"""

        await message.reply(response)