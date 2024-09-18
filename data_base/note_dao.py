from create_bot import logger
from .base import connection, get_or_create_tags
from .models import User, Note
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import List, Dict, Any, Optional


@connection
async def add_note_with_tags(session, user_id: int, content_type: str, tag_texts: List[str],
                             content_text: Optional[str] = None, file_id: Optional[str] = None) -> Optional[Note]:
    # Проверяем, существует ли пользователь с данным user_id
    user = await session.scalar(select(User).filter_by(id=user_id))
    if not user:
        logger.error(f"Пользователь с ID {user_id} не найден.")
        return None

    # Создаем новую заметку
    new_note = Note(
        user_id=user_id,
        content_type=content_type,
        content_text=content_text,
        file_id=file_id
    )

    # Получаем теги или создаем новые
    tags = await get_or_create_tags(session, tag_texts, tag_group='notes')
    new_note.tags.extend(tags)

    # Сохраняем изменения в базе данных с транзакцией
    async with session.begin():
        session.add(new_note)

    logger.info(f"Заметка для пользователя с ID {user_id} успешно добавлена!")
    return new_note


@connection
async def update_note(session, note_id: int, content_type: Optional[str] = None, content_text: Optional[str] = None,
                      file_id: Optional[str] = None, tag_texts: Optional[List[str]] = None) -> Optional[Note]:
    # Находим заметку
    note = await session.scalar(select(Note).filter_by(id=note_id))
    if not note:
        logger.error(f"Заметка с ID {note_id} не найдена.")
        return None

    # Обновляем поля заметки
    if content_type is not None:
        note.content_type = content_type
    if content_text is not None:
        note.content_text = content_text
    if file_id is not None:
        note.file_id = file_id

    # Обновляем теги, если указаны новые
    if tag_texts is not None:
        tags = await get_or_create_tags(session, tag_texts, tag_group='notes')
        note.tags = tags  # Обновляем только если теги изменились

    # Сохраняем изменения в базе данных
    await session.commit()
    logger.info(f"Заметка с ID {note_id} успешно обновлена!")
    return note


@connection
async def get_notes_by_user(session, user_id: int) -> List[Dict[str, Any]]:
    # Используем join для одновременного получения заметок и тегов, применяем joinedload для оптимизации
    result = await session.execute(
        select(Note).options(joinedload(Note.tags)).filter_by(user_id=user_id)
    )
    notes = result.scalars().all()

    if not notes:
        logger.info(f"Заметки для пользователя с ID {user_id} не найдены.")
        return []

    # Возвращаем заметки с тегами
    return [
        {
            'id': note.id,
            'content_type': note.content_type,
            'content_text': note.content_text,
            'file_id': note.file_id,
            'tags': [tag.tag_text for tag in note.tags]
        } for note in notes
    ]


@connection
async def get_note_by_id(session, note_id: int) -> Optional[Dict[str, Any]]:
    # Используем join для получения заметки и связанных с ней тегов, применяем joinedload
    result = await session.execute(
        select(Note).options(joinedload(Note.tags)).filter_by(id=note_id)
    )
    note = result.scalars().first()

    if not note:
        logger.info(f"Заметка с ID {note_id} не найдена.")
        return None

    # Возвращаем заметку с тегами
    return {
        'id': note.id,
        'content_type': note.content_type,
        'content_text': note.content_text,
        'file_id': note.file_id,
        'tags': [tag.tag_text for tag in note.tags]
    }


@connection
async def delete_note_by_id(session, note_id: int) -> Optional[Note]:
    # Находим заметку по id
    note = await session.get(Note, note_id)

    if not note:
        logger.error(f"Заметка с ID {note_id} не найдена.")
        return None

    # Удаляем заметку с транзакцией
    async with session.begin():
        await session.delete(note)

    logger.info(f"Заметка с ID {note_id} успешно удалена.")
    return note
