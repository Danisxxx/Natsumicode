import requests
from pyrogram import Client, filters

# URL de una API pública ficticia que no requiere clave
API_URL = "https://api.publicapis.org/phone_lookup"

def setup(bot):
    @bot.on_message(filters.command("dox"))
    def dox(client, message):
        try:
            # Obtener el número de teléfono del comando
            phone_number = message.text.split(" ")[1]

            # Realizar la solicitud a la API
            response = requests.get(API_URL, params={"phone": phone_number}, allow_redirects=False)

            # Verifica si hay una redirección
            if 300 <= response.status_code < 400:
                redirect_url = response.headers.get('Location')
                response = requests.get(redirect_url)

            # Procesar la respuesta
            data = response.json()

            # Verifica si la solicitud fue exitosa
            if response.status_code == 200 and data:
                # Extrae la información de la respuesta
                first_name = data.get("first_name", "Desconocido")
                last_name = data.get("last_name", "Desconocido")
                age = data.get("age", "Desconocido")
                country = data.get("country", "Desconocido")
                state = data.get("state", "Desconocido")
                city = data.get("city", "Desconocido")
                municipality = data.get("municipality", "Desconocido")
                id_number = data.get("id_number", "Desconocido")

                # Formatear y enviar el mensaje
                message_text = (f"⊛ Nombre : {first_name}\n"
                                f"⊛ Apellido: {last_name}\n"
                                f"⊛ Edad : {age}\n"
                                f"⊛ País 🇲🇽 : {country}\n"
                                f"⊛ Estado 👮‍♂️ : {state}\n"
                                f"⊛ Ciudad : {city}\n"
                                f"⊛ Municipio : {municipality}\n"
                                f"⊛ C.I : {id_number}")

                message.reply_text(message_text)
            else:
                message.reply_text("No se pudo obtener información para el número de teléfono proporcionado.")

        except Exception as e:
            message.reply_text(f"Error al procesar la solicitud: {e}")