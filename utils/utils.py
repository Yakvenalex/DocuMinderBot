import re

from aiogram.types import Message


def transform_string(input_string):
    # Разделяем строку по запятым
    words = input_string.split(',')
    # Убираем лишние пробелы, приводим к нижнему регистру и заменяем множественные пробелы на один
    cleaned_words = [re.sub(' +', ' ', word.strip().lower()) for word in words if word.strip()]
    # Объединяем слова обратно в строку через запятую
    result = ','.join(cleaned_words)
    return result


def get_content_info(message: Message):
    if message.photo:
        content_type = "photo"
        file_id = message.photo[-1].file_id
    elif message.video:
        content_type = "video"
        file_id = message.video.file_id
    elif message.audio:
        content_type = "audio"
        file_id = message.audio.file_id
    elif message.document:
        content_type = "document"
        file_id = message.document.file_id
    elif message.voice:
        content_type = "voice"
        file_id = message.voice.file_id
    elif message.text:
        content_type = "text"
        file_id = None
    else:
        return None
    text_content = message.text if message.text else message.caption
    return {'content_type': content_type, 'file_id': file_id, 'text_content': text_content}
