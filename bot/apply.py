# src/bot/apply.py
from telegram import Update
from telegram.ext import (
    Application,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from utils.validate import validate_name, validate_age, validate_city
from utils.logs import setup_logging

logger = setup_logging()

# Стани для ConversationHandler
NAME, AGE, PHOTOS, CITY = range(4)

async def start_application(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Розпочато подачу заявки. Введіть ваше ПІБ:")
    logger.info(f"Користувач {update.effective_user.id} почав подачу заявки")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    if validate_name(name):
        context.user_data["application"] = {"name": name}
        await update.message.reply_text("Введіть ваш вік:")
        logger.info(f"Користувач {update.effective_user.id} ввів ПІБ: {name}")
        return AGE
    else:
        await update.message.reply_text("Некоректне ПІБ. Введіть лише літери, пробіли чи дефіси:")
        return NAME

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age = update.message.text
    if validate_age(age):
        context.user_data["application"]["age"] = age
        await update.message.reply_text("Надішліть 2-3 фото з обличчям (по одному):")
        logger.info(f"Користувач {update.effective_user.id} ввів вік: {age}")
        context.user_data["photos"] = []
        return PHOTOS
    else:
        await update.message.reply_text("Некоректний вік. Введіть число від 16 до 100:")
        return AGE

async def get_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data["photos"].append(update.message.photo[-1].file_id)
        if len(context.user_data["photos"]) >= 2:
            await update.message.reply_text(
                "Отримано достатньо фото. Введіть ваше місто/область:"
            )
            logger.info(f"Користувач {update.effective_user.id} надіслав фото")
            return CITY
        else:
            await update.message.reply_text(
                f"Отримано {len(context.user_data['photos'])} фото. Надішліть ще одне:"
            )
            return PHOTOS
    else:
        await update.message.reply_text("Будь ласка, надішліть фото.")
        return PHOTOS

async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    if validate_city(city):
        context.user_data["application"]["city"] = city
        await update.message.reply_text(
            "Дякуємо! Заявку отримано, вона буде розглянута адміністраторами."
        )
        logger.info(f"Користувач {update.effective_user.id} завершив анкету: {context.user_data['application']}")
        # Тут буде збереження в Google Таблиці (реалізуємо пізніше)
        context.user_data.clear()
        return ConversationHandler.END
    else:
        await update.message.reply_text("Некоректне місто. Введіть назву міста/області:")
        return CITY

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Подачу заявки скасовано.")
    logger.info(f"Користувач {update.effective_user.id} скасував подачу заявки")
    context.user_data.clear()
    return ConversationHandler.END

def setup_application_handler(app: Application):
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("apply"), start_application)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            PHOTOS: [MessageHandler(filters.PHOTO, get_photos)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(conv_handler)