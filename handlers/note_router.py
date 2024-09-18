from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.reply_note_kb import main_note_kb

note_router = Router()


@note_router.message(F.text == '📝 Заметки')
async def cmd_start(message: Message):
    await message.answer('Ты в меню добавления заметок. Выбери необходимое действие.',
                         reply_markup=main_note_kb())
