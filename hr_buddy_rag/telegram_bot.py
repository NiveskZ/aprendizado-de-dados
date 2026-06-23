import os
import requests

from dotenv import load_dotenv
from pathlib import Path

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
FLOWISE_URL = os.getenv("FLOWISE_URL")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = update.message.text
    session_id = str(update.effective_user.id)

    resposta = requests.post(
        FLOWISE_URL,
        json={"question": mensagem,"streaming": False, "overrideConfig": {"sessionId": session_id}},
        timeout=30
    )
    await update.message.reply_text(resposta.json().get("text", "Erro ao processar."))

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()