from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from data_base.dao import delete_note_by_id, update_text_note
from keyboards.reply_note_kb import main_note_kb

upd_note_router = Router()


class UPDNoteStates(StatesGroup):
    content_text = State()


@upd_note_router.callback_query(F.data.startswith('dell_note_'))
async def dell_note_process(call: CallbackQuery, state: FSMContext):
    await state.clear()
    note_id = int(call.data.replace('dell_note_', ''))
    await delete_note_by_id(note_id=note_id)
    await call.answer(f'Заметка с ID {note_id} удалена!', show_alert=True)
    await call.message.delete()


@upd_note_router.callback_query(F.data.startswith('edit_note_text_'))
async def edit_note_text_process(call: CallbackQuery, state: FSMContext):
    await state.clear()
    note_id = int(call.data.replace('edit_note_text_', ''))
    await call.answer(f'Режим редактирования заметки с ID {note_id}')
    await state.update_data(note_id=note_id)
    await call.message.answer(f'Отправь новое текстовое содержимоем для заметки с ID {note_id}')
    await state.set_state(UPDNoteStates.content_text)


@upd_note_router.message(F.text, UPDNoteStates.content_text)
async def confirm_edit_note_text(message: Message, state: FSMContext):
    note_data = await state.get_data()
    note_id = note_data.get('note_id')
    content_text = message.text.strip()
    await update_text_note(note_id=note_id, content_text=content_text)
    await state.clear()
    await message.answer(f'Текст заметки с ID {note_id} успешно изменен на {content_text}!',
                         reply_markup=main_note_kb())
