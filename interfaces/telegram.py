import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

from core.brain import ArgosBrain

load_dotenv()

brain = ArgosBrain()

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = brain.think(user_message)
    except Exception as e:
        response = f"System error: {e}"

    await update.message.reply_text(response)


def run():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("👁️ Argos está vigilando...")
    app.run_polling()
