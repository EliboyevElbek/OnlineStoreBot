from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from Bot.telegram_bot3.config import DB_NAME
from Bot.telegram_bot3.keyboards.admin_inline_keyboards import make_categories_kb, make_confirm_kb
from Bot.telegram_bot3.states.admin_states import CategoryStates
from Bot.telegram_bot3.utils.database import Database


category_router = Router()
db = Database(DB_NAME)



@category_router.message(Command('categories'))
async def category_list_handler(message: Message):
    await message.answer(
        "Barcha kategorityalar:",
         reply_markup=make_categories_kb()
                        )


@category_router.message(Command('add_category'))
async def add_category_handler(message: Message, state: FSMContext):
    await state.set_state(CategoryStates.addCategoryState)
    await message.answer(text="Iltimos, yangi kategoriya nomini yuboring...")


@category_router.message(CategoryStates.addCategoryState)
async def insert_category_handler(message: Message, state=FSMContext):
    if db.check_category_exists(message.text):
        if db.add_category(new_category=message.text):
            await state.clear()
            await message.answer(
                f"Nomi bo'yicha yangi kategoriya '{message.text}' muvaffaqiyatli qo'shildi!"
            )
        else:
            await message.answer(
                f"Nimadir xato, kategoriyani qayta yuboring"
                f"Jarayonni bekor qilish uchun qayta yuboring yoki /cancel qilish tugmasini bosing!"
            )
    else:
        await message.answer(
            f"Kategoriya \"{message.text}\" allaqachon mavjud\n"
            f"Boshqa nomni yuboring yoki bosing /cancel bekor qilish jarayoni uchun!"
        )


@category_router.message(Command('edit_category'))
async def edit_category_handler(message: Message, state=FSMContext):
    await state.set_state(CategoryStates.startEditCategoryState)
    await message.answer(
        text="O'zgartirmoqchi bo'lgan toifani tanlang:",
        reply_markup=make_categories_kb()
    )


@category_router.callback_query(CategoryStates.startEditCategoryState)
async def select_category_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CategoryStates.finishEditCategoryState)
    await state.update_data(cat_name=callback.data)
    await callback.message.edit_text(f"Iltimos, kategoriya uchun yangi nom yuboring \"{callback.data}\":")


@category_router.message(CategoryStates.finishEditCategoryState)
async def update_category_handler(message: Message, state=FSMContext):
    if db.check_category_exists(message.text):
        all_data = await state.get_data()
        if db.rename_category(old_name=all_data.get('cat_name'), new_name=message.text):
            await state.clear()
            await message.answer(
                f"Kategoriya nomi muvaffaqiyatli o‘zgartirildi!"
            )
    else:
        await message.answer(
            f"Kategoriya \"{message.text}\" allaqachon mavjud\n"
            f"Boshqa nomni yuboring yoki bosing /cancel bekor qilish jarayoni uchun!"
        )


@category_router.message(Command('del_category'))
async def del_category_handler(message: Message, state=FSMContext):
    await state.set_state(CategoryStates.startDeleteCategoryState)
    await message.answer(
        text="O'chirmoqchi bo'lgan kategoriyani tanlang:",
        reply_markup=make_categories_kb()
    )


@category_router.callback_query(CategoryStates.startDeleteCategoryState)
async def select_category_del_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CategoryStates.finishDeleteCategoryState)
    await state.update_data(cat_name=callback.data)
    await callback.message.edit_text(
        text=f"Kategoriyani o'chirib tashlamoqchimisiz \"{callback.data}\":",
        reply_markup=make_confirm_kb()
    )


@category_router.callback_query(CategoryStates.finishDeleteCategoryState)
async def remove_category_handler(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'HA':
        all_data = await state.get_data()
        if db.delete_category(all_data.get('cat_name')):
            await callback.message.answer("Kategoriya muvaffaqiyatli oʻchirildi!")
            await callback.message.delete()
            await state.clear()
        else:
            await callback.message.answer(
                f"Nimadir noto'g'ri bajarildi!"
                f"Keyinroq qayta urining yoki bosing /cancel bekor qilish jarayoni uchun!"
            )
    else:
        await state.clear()
        await callback.message.answer('Jarayon bekor qilindi!')
        await callback.message.delete()