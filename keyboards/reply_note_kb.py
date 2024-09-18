from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_note_kb():
    kb_list = [
        [KeyboardButton(text="📝 Добавить заметку"), KeyboardButton(text="📋 Просмотр заметок")],
        [KeyboardButton(text="🏠 Главное меню")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйся меню👇"
    )


def note_find_kb():
    kb_list = [
        [KeyboardButton(text="📚 Все заметки")],
        [KeyboardButton(text="📅 Заметки по дате добавления"), KeyboardButton(text="🏷️ Заметки по тегу")],
        [KeyboardButton(text="🏠 Главное меню")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйся меню👇"
    )
