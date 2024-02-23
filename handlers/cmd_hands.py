from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from Bot.telegram_bot3.config import admins
from Bot.telegram_bot3.utils.my_commands import admin_commands, user_commands

cmd_router = Router()



@cmd_router.message(CommandStart())
async def start_handler(message: Message):
    if message.from_user.id in admins:
        await message.bot.set_my_commands(commands=admin_commands)
        await message.answer("Xushkelibsiz! Admin")
    else:
        await message.bot.set_my_commands(commands=user_commands)
        await message.answer("Xushkelibsiz!")


@cmd_router.message(Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Barchasi bekor qilindi!")
