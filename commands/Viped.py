import sqlite3
from pyrogram import Client, filters
from datetime import datetime, timedelta
import threading
import time

def setup(client):
    @client.on_message(filters.command("vip"))
    def vip_command(client, message):
        try:
            user_id = message.from_user.id
            user_data = get_user_data(user_id)
            
            if user_data['poder'] not in ['Owner', 'Seller', 'Admin']:
                message.reply("**Lo siento, no tienes permiso para usar este comando** ❌")
                return
            
            args = message.text.split()
            if len(args) < 3:
                message.reply("**Uso incorrecto del comando. Usa: /vip ID Dias [Creditos]**")
                return
            
            target_user_id = args[1]
            try:
                days = int(args[2])
                credits = int(args[3]) if len(args) == 4 else None
            except ValueError:
                message.reply("**Días y créditos deben ser números enteros**")
                return
            
            with sqlite3.connect('/storage/emulated/0/Download/Natsumichkbot/Natsumi.db') as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM registered_users WHERE Id = ?", (target_user_id,))
                user = cursor.fetchone()
                
                if user is None:
                    message.reply("**Usuario no encontrado**")
                    return
                
                current_seconds = parse_duration(user[4]) if user[4] else 0
                added_seconds = days * 86400  # Convertir días a segundos

                if days == 0 and credits is None:
                    if user[3] in ['Owner', 'Seller', 'Admin']:
                        cursor.execute("""
                            UPDATE registered_users
                            SET dias = '0d-00h-00m-00s'
                            WHERE Id = ?
                        """, (target_user_id,))
                        conn.commit()
                        confirmation_message = (
                            f"**Al Usuario Con ID** <code>{target_user_id}</code> **Se Le Han Quitado Los Días Del Plan VIP**!\n"
                            f"**Días**: 0\n"
                            f"**Créditos**: {user[5]}\n"
                            f"**Promovido Por**: @{message.from_user.username} [{user_data['poder']}]"
                        )
                    else:
                        cursor.execute("""
                            UPDATE registered_users
                            SET rango = 'Free User',
                                dias = '0d-00h-00m-00s',
                                AntiSpam = 40
                            WHERE Id = ?
                        """, (target_user_id,))
                        conn.commit()
                        confirmation_message = (
                            f"**Al Usuario Con ID** <code>{target_user_id}</code> **Se Le Han Quitado Los Días Del Plan VIP y Su Rango Ha Sido Revertido a Free User**!\n"
                            f"**Días**: 0\n"
                            f"**Créditos**: {user[5]}\n"
                            f"**Promovido Por**: @{message.from_user.username} [{user_data['poder']}]"
                        )
                
                elif days == 0 and credits == 0:
                    if user[3] in ['Owner', 'Seller', 'Admin']:
                        cursor.execute("""
                            UPDATE registered_users
                            SET dias = '0d-00h-00m-00s',
                                creditos = 0
                            WHERE Id = ?
                        """, (target_user_id,))
                        conn.commit()
                        confirmation_message = (
                            f"**Al Usuario Con ID** <code>{target_user_id}</code> **Se Le Han Quitado Los Días y Créditos Del Plan VIP**!\n"
                            f"**Días**: 0\n"
                            f"**Créditos**: 0\n"
                            f"**Promovido Por**: @{message.from_user.username} [{user_data['poder']}]"
                        )
                    else:
                        cursor.execute("""
                            UPDATE registered_users
                            SET rango = 'Free User',
                                dias = '0d-00h-00m-00s',
                                creditos = 0,
                                AntiSpam = 40
                            WHERE Id = ?
                        """, (target_user_id,))
                        conn.commit()
                        confirmation_message = (
                            f"**Al Usuario Con ID** <code>{target_user_id}</code> **Se Le Han Quitado Los Días y Créditos Del Plan VIP y Su Rango Ha Sido Revertido a Free User**!\n"
                            f"**Días**: 0\n"
                            f"**Créditos**: 0\n"
                            f"**Promovido Por**: @{message.from_user.username} [{user_data['poder']}]"
                        )
                
                else:
                    new_seconds = current_seconds + added_seconds
                    new_credits = int(user[5]) + credits if credits is not None else user[5]

                    cursor.execute("""
                        UPDATE registered_users
                        SET rango = 'VIP',
                            dias = ?,
                            creditos = ?,
                            AntiSpam = 15
                        WHERE Id = ?
                    """, (format_duration(new_seconds), new_credits, target_user_id))
                    conn.commit()

                    confirmation_message = (
                        f"La ID <code>{target_user_id}</code> ha sido promovida al plan VIP!\n"
                        f"Días: <code>{days}</code>\n"
                        f"Créditos: <code>{credits if credits is not None else 0}</code>\n"
                        f"Promovido Por: @{message.from_user.username} [<code>{user_data['poder']}</code>]"
                    )
                
                message.reply(confirmation_message)
        
        except sqlite3.Error as e:
            message.reply(f"Error de base de datos: {e}")
        
        except Exception as e:
            message.reply(f"Error inesperado: {str(e)}")

def get_user_data(user_id):
    try:
        with sqlite3.connect('/storage/emulated/0/Download/Natsumichkbot/Natsumi.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT poder FROM registered_users WHERE Id = ?", (user_id,))
            user = cursor.fetchone()
            if user:
                return {'poder': user[0]}
            return {'poder': None}
    
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        return {'poder': None}
    
    except Exception as e:
        print(f"Error inesperado: {e}")
        return {'poder': None}

def parse_duration(duration_str):
    """Convierte una cadena de duración en segundos."""
    days, hours, minutes, seconds = 0, 0, 0, 0
    if duration_str:
        parts = duration_str.split('-')
        for part in parts:
            if 'd' in part:
                days = int(part.replace('d', ''))
            elif 'h' in part:
                hours = int(part.replace('h', ''))
            elif 'm' in part:
                minutes = int(part.replace('m', ''))
            elif 's' in part:
                seconds = int(part.replace('s', ''))
    total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
    return total_seconds

def format_duration(total_seconds):
    """Convierte segundos en una cadena de duración en formato 'Xd-Yh-Zm-Ws'."""
    days = total_seconds // 86400
    total_seconds %= 86400
    hours = total_seconds // 3600
    total_seconds %= 3600
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{days}d-{hours}h-{minutes}m-{seconds}s"

def update_time():
    """Actualiza el tiempo en la base de datos en tiempo real."""
    while True:
        with sqlite3.connect('/storage/emulated/0/Download/Natsumichkbot/Natsumi.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Id, dias FROM registered_users")
            users = cursor.fetchall()
            for user_id, duration_str in users:
                current_seconds = parse_duration(duration_str)
                new_seconds = current_seconds - 1
                if new_seconds <= 0:
                    new_duration = '0d-00h-00m-00s'
                else:
                    new_duration = format_duration(new_seconds)
                cursor.execute("""
                    UPDATE registered_users
                    SET dias = ?
                    WHERE Id = ?
                """, (new_duration, user_id))
            conn.commit()
        time.sleep(1)

if __name__ == "__main__":
    # Inicia el hilo para actualizar el tiempo
    update_thread = threading.Thread(target=update_time)
    update_thread.start()
