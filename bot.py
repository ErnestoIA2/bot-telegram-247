import os, threading, telebot
from groq import Groq
from flask import Flask

TOKEN = os.environ["TELEGRAM_TOKEN"]
GROQ = os.environ["GROQ_API_KEY"]

bot = telebot.TeleBot(TOKEN)
client = Groq(api_key=GROQ)
app = Flask(__name__)

@app.route("/")
def alive():
    return "✅ Bot vivo", 200

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, f"¡Hola {m.from_user.first_name}! 👋 Escribe tu pregunta.")

@bot.message_handler(func=lambda m: True)
def responder(m):
    bot.reply_to(m, "🧠 Pensando...")
    try:
        r = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":m.text}], max_tokens=300)
        bot.reply_to(m, r.choices[0].message.content)
    except Exception as e:
        bot.reply_to(m, f"⚠️ Error: {e}")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080), daemon=True).start()
    print("✅ Bot activo...")
    bot.infinity_polling(timeout=10, skip_pending=True)