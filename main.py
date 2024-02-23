import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from Bot.telegram_bot3.handlers.category_handler import category_router
from Bot.telegram_bot3.handlers.cmd_hands import cmd_router
from config import BOT_TOKEN


async def main():
    bot = Bot(
        token=BOT_TOKEN,
        parse_mode=ParseMode.HTML
    )
    dp = Dispatcher()
    dp.include_routers(cmd_router, category_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except:
        print('Bot stop')