# bot/welcome.py
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in ADMIN_IDS:
        await update.message.reply_text("Вітаю, адмін! Скоро тут буде адмін-панель.")
    else:
        await update.message.reply_text("Вітаю! Це бот для ознайомлення зі спільнотою Krendels. Скоро додамо меню!")