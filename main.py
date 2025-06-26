# main.py
from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from bot.welcome import start
from utils.logs import setup_logging

logger = setup_logging()

def main():
    logger.info("Бот запускається")
    app = Application.builder().token(BOT_TOKEN).build()
    logger.info("Application ініціалізовано")
    app.add_handler(CommandHandler("start", start))
    logger.info("Обробник команди /start додано")
    app.run_polling(allowed_updates=["message", "callback_query"])
    logger.info("Polling запущено")

if __name__ == "__main__":
    main()