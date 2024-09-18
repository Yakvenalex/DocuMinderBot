from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from keyboards.reply_note_kb import main_note_kb
from keyboards.reply_other_kb import stop_fsm
from utils.utils import get_content_info

note_router = Router()


class AddNoteStates(StatesGroup):
    content = State()  # Ожидаем любое сообщение от пользователя
    tags = State()  # Ожидаем ввод тегов товара
    check_state = State()  # Финальна проверка


@note_router.message(F.text == '📝 Заметки')
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Ты в меню добавления заметок. Выбери необходимое действие.',
                         reply_markup=main_note_kb())


@note_router.message(F.text == '📝 Добавить заметку')
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Отправь сообщение в любом формате (текст, медиа или медиа + текст). '
                         'В случае если к медиа требуется подпись - оставь ее в комментариях к медиа-файлу ',
                         reply_markup=stop_fsm())
    await state.set_state(AddNoteStates.content)


@note_router.message(AddNoteStates.content)
async def handle_user_note_message(message: Message, state: FSMContext):
    content_info = get_content_info(message)
    if content_info:
        await state.update_data(**content_info)
        await message.answer(
            f"Получена заметка:\n"
            f"Тип: {content_info['content_type']}\n"
            f"Подпись: {content_info['text_content'] if content_info['text_content'] else 'Отсутствует'}\n"
            f"File ID: {content_info['file_id'] if content_info['file_id'] else 'Нет файла'}\n\n"
            f"Теперь выберите тег к записи из ",
            reply_markup=main_note_kb())
        await state.set_state(AddNoteStates.tags)
    else:
        await message.answer(
            'Не удалось получить содержимое сообщения. Пожалуйста, отправьте сообщение в любом формате.'
        )
        await state.set_state(AddNoteStates.content)
