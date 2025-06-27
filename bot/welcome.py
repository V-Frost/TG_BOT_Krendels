# src/bot/welcome.py
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from config import ADMIN_IDS
from utils.logs import setup_logging
from utils.buttons import get_user_menu, get_admin_menu

logger = setup_logging()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    greeting = "Вітаю! Це бот для ознайомлення зі спільнотою\n☀️🥨ДЕЛОВЫЕ КРЕНДЕЛИ🥨☀️"
    reply_markup = get_admin_menu() if user_id in ADMIN_IDS else get_user_menu()
    
    await update.message.reply_photo(
        photo=open("krendels.jpg", "rb"),
        caption=greeting,
        reply_markup=reply_markup
    )
    
    logger.info(f"{'Адмін' if user_id in ADMIN_IDS else 'Користувач'} {user_id} викликав /start")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    if query.data == "info":
        await query.message.reply_text("Це спільнота Krendels! Тут ми ділимося ідеями та спілкуємося.")
        logger.info(f"Користувач {user_id} вибрав 'Ознайомитися'")
    elif query.data == "apply":
        await query.message.reply_text("Розпочато подачу заявки. Введіть ваше ПІБ:")
        logger.info(f"Користувач {user_id} вибрав 'Подати заявку'")
    elif query.data == "view_applications" and user_id in ADMIN_IDS:
        await query.message.reply_text("Список заявок буде тут (у розробці).")
        logger.info(f"Адмін {user_id} вибрав 'Переглянути заявки'")
    else:
        await query.message.reply_text("Ця дія доступна лише адміністраторам.")
        logger.warning(f"Користувач {user_id} намагався отримати доступ до адмінської функції")