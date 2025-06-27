# src/main.py
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN
from bot.welcome import start, button_callback
from bot.apply import setup_application_handler
from utils.logs import setup_logging

logger = setup_logging()

def main():
    logger.info("Бот запускається")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    setup_application_handler(app)
    logger.info("Обробники для /start, кнопок і анкети додано")
    app.run_polling(allowed_updates=["message", "callback_query"])
    logger.info("Polling запущено")

if __name__ == "__main__":
    main()