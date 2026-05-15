#!/usr/bin/env python3
import os, sys, telebot
from groq import Groq

# === CONFIGURACIÓN ===
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_KEY = os.environ.get("GROQ_API_KEY")

if not TOKEN or not GROQ_KEY:
    print("❌ ERROR: Faltan TELEGRAM_TOKEN o GROQ_API_KEY")
    sys.exit(1)

print("✅ Claves OK. Iniciando bot...")

# === INICIALIZACIÓN ===
bot = telebot.TeleBot(TOKEN, skip_pending=True, timeout=30)
client = Groq(api_key=GROQ_KEY)

# === COMANDOS ===
@bot.message_handler(commands=['start', 'help'])
def start(m):
    bot.reply_to(m, f"¡Hola {m.from_user.first_name}! 👋\nEscribe tu pregunta.")

# === RESPUESTAS CON IA ===
@bot.message_handler(func=lambda m: True)
def responder(m):
    try:
        bot.send_chat_action(m.chat.id, 'typing')
        r = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"user","content":m.text}],
            max_tokens=400
        )
        bot.reply_to(m, r.choices[0].message.content)
        print(f"✅ Respondido")
    except Exception as e:
        print(f"❌ Error: {e}")
        bot.reply_to(m, "⚠️ Error temporal. Intenta de nuevo.")

# === EJECUCIÓN ===
if __name__ == "__main__":
    print("🚀 Bot conectado. Esperando mensajes...")
    bot.infinity_polling(timeout=30)
