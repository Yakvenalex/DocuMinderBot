from datetime import date, time
from create_bot import logger
from .base import connection, get_or_create_tags
from .models import User, Reminder
from sqlalchemy import select
from sqlalchemy.orm import joinedload, aliased
from typing import List, Dict, Any, Optional


@connection
async def add_reminder(session, user_id: int, content: str, reminder_date: date, reminder_time: time,
                       tag_texts: List[str]) -> Optional[Reminder]:
    # Проверяем, существует ли пользователь с данным user_id
    user = await session.scalar(select(User).filter_by(id=user_id))
    if not user:
        logger.error(f"Пользователь с ID {user_id} не найден.")
        return None

    # Создаем новое напоминание
    new_reminder = Reminder(
        user_id=user_id,
        content_text=content,
        reminder_date=reminder_date,
        reminder_time=reminder_time
    )

    # Получаем теги или создаем новые
    tags = await get_or_create_tags(session, tag_texts, tag_group='reminders')
    new_reminder.tags.extend(tags)

    # Сохраняем изменения в базе данных с транзакцией
    async with session.begin():
        session.add(new_reminder)

    logger.info(f"Напоминание для пользователя с ID {user_id} успешно добавлено!")
    return new_reminder


@connection
async def update_reminder(session, reminder_id: int, content: Optional[str] = None, reminder_date: Optional[str] = None,
                          reminder_time: Optional[str] = None, tag_texts: Optional[List[str]] = None) -> Optional[
    Reminder]:
    # Находим напоминание
    reminder = await session.scalar(select(Reminder).filter_by(id=reminder_id))
    if not reminder:
        logger.error(f"Напоминание с ID {reminder_id} не найдено.")
        return None

    # Обновляем поля напоминания
    if content is not None:
        reminder.content_text = content
    if reminder_date is not None:
        reminder.reminder_date = reminder_date
    if reminder_time is not None:
        reminder.reminder_time = reminder_time

    # Обновляем теги
    if tag_texts is not None:
        tags = await get_or_create_tags(session, tag_texts, tag_group='reminders')
        reminder.tags = tags

    # Сохраняем изменения в базе данных
    await session.commit()
    logger.info(f"Напоминание с ID {reminder_id} успешно обновлено!")
    return reminder


@connection
async def get_reminders_by_user(session, user_id: int) -> List[Dict[str, Any]]:
    # Используем join для одновременного получения напоминаний и тегов, применяем joinedload для оптимизации
    result = await session.execute(
        select(Reminder).options(joinedload(Reminder.tags)).filter_by(user_id=user_id)
    )
    reminders = result.scalars().all()

    if not reminders:
        logger.info(f"Напоминания для пользователя с ID {user_id} не найдены.")
        return []

    # Возвращаем напоминания с тегами
    return [
        {
            'id': reminder.id,
            'content_text': reminder.content_text,
            'reminder_date': reminder.reminder_date,
            'reminder_time': reminder.reminder_time,
            'tags': [tag.tag_text for tag in reminder.tags]
        } for reminder in reminders
    ]


@connection
async def get_reminder_by_id(session, reminder_id: int) -> Optional[Dict[str, Any]]:
    # Используем join для получения напоминания и связанных с ним тегов, применяем joinedload
    result = await session.execute(
        select(Reminder).options(joinedload(Reminder.tags)).filter_by(id=reminder_id)
    )
    reminder = result.scalars().first()

    if not reminder:
        logger.info(f"Напоминание с ID {reminder_id} не найдено.")
        return None

    # Возвращаем напоминание с тегами
    return {
        'id': reminder.id,
        'content_text': reminder.content_text,
        'reminder_date': reminder.reminder_date,
        'reminder_time': reminder.reminder_time,
        'tags': [tag.tag_text for tag in reminder.tags]
    }


@connection
async def delete_reminder_by_id(session, reminder_id: int) -> Optional[Reminder]:
    # Находим напоминание по id
    reminder = await session.get(Reminder, reminder_id)

    if not reminder:
        logger.error(f"Напоминание с ID {reminder_id} не найдено.")
        return None

    # Удаляем напоминание с транзакцией
    async with session.begin():
        await session.delete(reminder)

    logger.info(f"Напоминание с ID {reminder_id} успешно удалено.")
    return reminder


@connection
async def get_tag_tree_reminder_for_user(session, user_id: int) -> List[Dict[str, Any]]:
    # Запрос для получения тегов и их связанных напоминаний для конкретного пользователя
    result = await session.execute(
        select(Reminder.id, Reminder.tags)  # Выбираем id напоминания и теги
        .filter_by(user_id=user_id)  # Условие фильтрации по user_id
        .options(joinedload(Reminder.tags))  # Загружаем связанные теги
    )

    reminders = result.scalars().all()

    # Если напоминания не найдены
    if not reminders:
        logger.info(f"Теги для пользователя с ID {user_id} не найдены.")
        return []

    # Формируем дерево тегов
    tag_tree = []
    for reminder in reminders:
        tag_tree.append({
            'reminder_id': reminder.id,
            'tags': [tag.tag_text for tag in reminder.tags]
        })

    return tag_tree
