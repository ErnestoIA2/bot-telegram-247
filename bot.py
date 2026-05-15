import os, sys, threading, telebot
from groq import Groq
from flask import Flask

# Lectura segura
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_KEY = os.environ.get("GROQ_API_KEY")

if not TOKEN:
    print("❌ ERROR: TELEGRAM_TOKEN no está definido")
    sys.exit(1)
if not GROQ_KEY:
    print("❌ ERROR: GROQ_API_KEY no está definido")
    sys.exit(1)

print(f"✅ Claves cargadas. Token inicia con: {TOKEN[:10]}...")

bot = telebot.TeleBot(TOKEN, skip_pending=True)
client = Groq(api_key=GROQ_KEY)
app = Flask(__name__)

@app.route("/")
def alive():
    return "✅ Bot vivo", 200

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, f"¡Hola {m.from_user.first_name}! 👋 Escribe tu pregunta.")

@bot.message_handler(func=lambda m: True)
def responder(m):
    try:
        r = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"user","content":m.text}],
            max_tokens=300
        )
        bot.reply_to(m, r.choices[0].message.content)
    except Exception as e:
        print(f"❌ Error en IA: {e}")
        bot.reply_to(m, "⚠️ Error temporal. Intenta de nuevo.")

if __name__ == "__main__":
    # Inicia Flask en hilo separado
    def run_flask():
        app.run(host="0.0.0.0", port=8080, log_level="error")
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("✅ Bot activo. Esperando mensajes...")
    try:
        bot.infinity_polling(timeout=10)
    except Exception as e:
        print(f"❌ Bot detenido: {e}")
        sys.exit(1)
