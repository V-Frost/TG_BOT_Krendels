# src/utils/buttons.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMIN_IDS

def get_user_menu():
    buttons = [
        [InlineKeyboardButton("Ознайомитися зі спільнотою", callback_data="info")],
        [InlineKeyboardButton("Подати заявку", callback_data="apply")]
    ]
    return InlineKeyboardMarkup(buttons)

def get_admin_menu():
    buttons = [
        [InlineKeyboardButton("Ознайомитися зі спільнотою", callback_data="info")],
        [InlineKeyboardButton("Подати заявку", callback_data="apply")],
        [InlineKeyboardButton("Переглянути заявки", callback_data="view_applications")]
    ]
    return InlineKeyboardMarkup(buttons)