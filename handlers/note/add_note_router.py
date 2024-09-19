from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from create_bot import bot
from data_base.dao import add_note
from keyboards.reply_note_kb import main_note_kb, add_note_check
from keyboards.reply_other_kb import stop_fsm
from utils.utils import get_content_info, send_message_user

add_note_router = Router()


class AddNoteStates(StatesGroup):
    content = State()  # Ожидаем любое сообщение от пользователя
    check_state = State()  # Финальна проверка


@add_note_router.message(F.text == '📝 Заметки')
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Ты в меню добавления заметок. Выбери необходимое действие.',
                         reply_markup=main_note_kb())


@add_note_router.message(F.text == '📝 Добавить заметку')
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Отправь сообщение в любом формате (текст, медиа или медиа + текст). '
                         'В случае если к медиа требуется подпись - оставь ее в комментариях к медиа-файлу ',
                         reply_markup=stop_fsm())
    await state.set_state(AddNoteStates.content)


@add_note_router.message(AddNoteStates.content)
async def handle_user_note_message(message: Message, state: FSMContext):
    content_info = get_content_info(message)
    if content_info.get('content_type'):
        await state.update_data(**content_info)

        text = (f"Получена заметка:\n"
                f"Тип: {content_info['content_type']}\n"
                f"Подпись: {content_info['content_text'] if content_info['content_text'] else 'Отсутствует'}\n"
                f"File ID: {content_info['file_id'] if content_info['file_id'] else 'Нет файла'}\n\n"
                f"Все ли верно?")
        await send_message_user(bot=bot, content_type=content_info['content_type'], content_text=text,
                                user_id=message.from_user.id, file_id=content_info['file_id'],
                                kb=add_note_check())
        await state.set_state(AddNoteStates.check_state)
    else:
        await message.answer(
            'Я не знаю как работать с таким медафайлом, как ты скинул. Давай что-то другое, ок?'
        )
        await state.set_state(AddNoteStates.content)


@add_note_router.message(AddNoteStates.check_state, F.text == '✅ Все верно')
async def confirm_add_note(message: Message, state: FSMContext):
    note = await state.get_data()
    await add_note(user_id=message.from_user.id, content_type=note.get('content_type'),
                   content_text=note.get('content_text'), file_id=note.get('file_id'))
    await message.answer('Заметка успешно добавлена!', reply_markup=main_note_kb())
    await state.clear()


@add_note_router.message(AddNoteStates.check_state, F.text == '❌ Отменить')
async def cancel_add_note(message: Message, state: FSMContext):
    await message.answer('Добавление заметки отменено!', reply_markup=main_note_kb())
    await state.clear()
