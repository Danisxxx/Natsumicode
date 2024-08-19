import time
import stripe
from pyrogram import Client, filters

# Configura tu clave de API de Stripe
stripe.api_key = "sk_test_51Pjb6lDQqf4qA8JhBOBuEbvDWA37dybOQEVPxDONDkguj6WmlBMxEojP1Rpo3yti8bxXEYAZeOnuqPfCTP7vhUU0008jXNPFBZ"  # Reemplaza con tu clave secreta de Stripe

# Archivos de configuración
AUTHORIZED_GROUPS_FILE = "/storage/emulated/0/Download/Natsumichkbot/commands/GroupAutorize.txt"
VIPED_IDS_FILE = "/storage/emulated/0/Download/Natsumichkbot/commands/Viped.txt"

def extract_ids(file_path, is_group=False):
    """
    Extrae los IDs del archivo, filtrando solo los valores numéricos.
    """
    ids = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                # Si se está extrayendo IDs de grupos, se permiten valores negativos (IDs de grupos)
                if is_group:
                    if line.strip().startswith('-'):
                        ids.append(int(line.strip()))
                else:
                    # Para usuarios VIP, extraer el primer valor numérico
                    parts = line.split()
                    if parts and parts[0].isdigit():
                        ids.append(int(parts[0]))
    except FileNotFoundError:
        pass
    return ids

def setup(client):
    @client.on_message(filters.command(["vbv", ".vbv"], prefixes=["/", "."]))
    async def vbv_command(client, message):
        start_time = time.time()

        # Leer los IDs de grupos autorizados
        authorized_group_ids = extract_ids(AUTHORIZED_GROUPS_FILE, is_group=True)

        # Leer los IDs VIP
        viped_ids = extract_ids(VIPED_IDS_FILE)

        # Verificar si el mensaje proviene de un chat de grupo o privado
        is_group = message.chat.type in ["group", "supergroup"]
        user_id = message.from_user.id

        if is_group:
            if message.chat.id not in authorized_group_ids:
                await message.reply("Compra una membresía para usar este comando en grupos.")
                return
        else:
            if user_id not in viped_ids:
                await message.reply("Compra una membresía para usar este comando en el chat privado.")
                return

        # Verificar si el usuario proporcionó una tarjeta
        if len(message.command) < 2:
            await message.reply("Por favor, proporciona una tarjeta en el formato correcto.")
            return

        card_info = message.command[1]
        card_details = card_info.split("|")

        if len(card_details) != 4:
            await message.reply("Formato incorrecto. Usa el formato: 1234567890123456|MM|YYYY|CVV")
            return

        # Enviar el mensaje inicial de "CHECKING CARD"
        checking_message = await message.reply("🔄 Chequeando tarjeta...")

        card_number = card_details[0].strip()
        exp_month = int(card_details[1].strip())  # Asegúrate de que exp_month sea un entero
        exp_year = int(card_details[2].strip())   # Asegúrate de que exp_year sea un entero
        cvv = card_details[3].strip()

        # Consultar información del 3D Secure con Stripe
        try:
            # Crear un PaymentIntent para verificar si se requiere autenticación adicional
            payment_intent = stripe.PaymentIntent.create(
                amount=1000,  # Monto en centavos, ajusta según sea necesario
                currency="usd",  # Moneda, ajusta según sea necesario
                payment_method={
                    "type": "card",
                    "card": {
                        "number": card_number,
                        "exp_month": exp_month,
                        "exp_year": exp_year,
                        "cvc": cvv
                    }
                },
                confirm=True  # Confirmar el PaymentIntent inmediatamente
            )

            # Verificar si se requiere autenticación
            if payment_intent.status in ["requires_action", "requires_source_action"]:
                result_message = (
                    f"bin ➜ {card_number[:6]}\n"
                    f"Result ➜ Declined ❌\n"
                    f"Gateway ➜ Stripe 3D Secure\n"
                    f"- - - - - - - - - - - - - - - - - - - - - - - -\n"
                    f"Response ➜ La tarjeta requiere autenticación adicional.\n"
                )
            else:
                result_message = (
                    f"bin ➜ {card_number[:6]}\n"
                    f"Result ➜ Approved ✅\n"
                    f"Gateway ➜ Stripe 3D Secure\n"
                    f"- - - - - - - - - - - - - - - - - - - - - - - -\n"
                    f"Response ➜ La tarjeta fue aprobada y no requiere 3D Secure.\n"
                )

        except stripe.error.CardError as e:
            result_message = (
                f"bin ➜ {card_number[:6]}\n"
                f"Result ➜ Declined ❌\n"
                f"Gateway ➜ Stripe 3D Secure\n"
                f"- - - - - - - - - - - - - - - - - - - - - - - -\n"
                f"Response ➜ {e.error.message}\n"
            )
        except Exception as e:
            result_message = (
                f"bin ➜ {card_number[:6]}\n"
                f"Result ➜ Error ⚠️\n"
                f"Gateway ➜ Stripe 3D Secure\n"
                f"- - - - - - - - - - - - - - - - - - - - - - - -\n"
                f"Response ➜ {str(e)}\n"
            )

        # Tiempo de ejecución
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)

        # Añadir información del tiempo de ejecución al mensaje
        result_message += (
            f"- - - - - - - - - - - - - - - - - - - - - - - -\n"
            f"Checked by ➜ @{message.from_user.username}{'[VIP]' if user_id in viped_ids else '[FREE]'}\n"
            f"Test Time ➜ {execution_time}s"
        )

        # Editar el mensaje de "CHECKING CARD" con el resultado final
        await checking_message.edit_text(result_message)
