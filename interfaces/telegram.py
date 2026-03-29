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
        # 1. Obtenemos la respuesta del cerebro
        response = brain.think(user_message)
        
        # 2. RED DE SEGURIDAD: Si la respuesta viene vacía o nula
        if not response or not response.strip():
            response = "Estado nominal. Procesando datos en segundo plano."
            
    except Exception as e:
        # Si algo falla en el cerebro, Argos informa con su estilo
        response = f"Fallo en enlace neuronal: {e}"

    # 3. Ahora estamos seguros de que 'response' nunca será una cadena vacía
    await update.message.reply_text(response)


def run():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("❌ Error: No se encontró TELEGRAM_TOKEN en el archivo .env")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("Initializing Argos...")
    print("👁️ Argos está vigilando...")
    app.run_polling()
