from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Bot.telegram_bot3.config import DB_NAME
from Bot.telegram_bot3.utils.database import Database

db = Database(DB_NAME)



def make_categories_kb():
    categories = db.get_categories()
    rows = []
    for cat in categories:
        rows.append([
            InlineKeyboardButton(
                text=cat[1], callback_data=str(cat[1])
            )]
        )
    inl_kb = InlineKeyboardMarkup(
        inline_keyboard=rows
    )
    return inl_kb


def make_confirm_kb():
    rows = [
        InlineKeyboardButton(text='HA', callback_data='HA'),
        InlineKeyboardButton(text='YO\'Q', callback_data='YO\'Q')
    ]
    inl_kb = InlineKeyboardMarkup(
        inline_keyboard=[rows]
    )
    return inl_kb