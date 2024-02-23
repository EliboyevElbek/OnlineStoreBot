from aiogram.types import BotCommand

admin_commands = [
    BotCommand(command='start', description='Boshlash'),
    BotCommand(command='categories', description='Barcha kategoriyalar'),
    BotCommand(command='add_category', description='Kategoriya qo\'shish'),
    BotCommand(command='edit_category', description='O\'zgartirish'),
]

user_commands = [
    BotCommand(command='start', description='Boshlash'),
    BotCommand(command='help', description='Bot haqida'),
]