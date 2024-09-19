from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from data_base.dao import set_user
from keyboards.reply_other_kb import main_kb

start_router = Router()


# Хендлер команды /start и кнопки "🏠 Главное меню"
@start_router.message(F.text == '🏠 Главное меню')
@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user = await set_user(tg_id=message.from_user.id,
                          username=message.from_user.username,
                          full_name=message.from_user.full_name)
    greeting = f"Привет, {message.from_user.full_name}! Выбери необходимое действие"
    if user is None:
        greeting = f"Привет, новый пользователь! Выбери необходимое действие"

    await message.answer(greeting, reply_markup=main_kb())


@start_router.message(F.text == '❌ Остановить сценарий')
async def stop_fsm(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Сценарий остановлен. Для выбора действия воспользуйся клавиатурой ниже",
                         reply_markup=main_kb())


@start_router.callback_query(F.data == 'main_menu')
async def main_menu_process(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer('Вы вернулись в главное меню.')
    await call.message.answer(f"Привет, {call.from_user.full_name}! Выбери необходимое действие",
                              reply_markup=main_kb())
