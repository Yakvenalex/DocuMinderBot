import aiosqlite

from create_bot import db_file


def get_reminder_dict(row):
    return {'id': row[0], 'user_id': row[1], 'text_content': row[2], 'reminder_date': row[3],
            'reminder_time': row[4], 'tags': row[5], 'created_at': row[6], 'updated_at': row[7]
            }


# Функция для добавления напоминания
async def add_reminder(user_id, text_content, reminder_date, reminder_time, tags):
    async with aiosqlite.connect(db_file) as db:
        await db.execute('''
            INSERT INTO reminders (user_id, text_content, reminder_date, reminder_time, tags)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, text_content, reminder_date, reminder_time, tags))
        await db.commit()


# Функция для получения всех напоминаний пользователя
async def get_all_reminders_by_user(user_id):
    async with aiosqlite.connect(db_file) as db:
        async with db.execute('SELECT * FROM reminders WHERE user_id = ?', (user_id,)) as cursor:
            reminders = []
            async for row in cursor:
                reminders.append(get_reminder_dict(row))
            return reminders


# Функция для поиска напоминаний по дате
async def get_reminders_by_date(date, user_id):
    async with aiosqlite.connect(db_file) as db:
        async with db.execute('SELECT * FROM reminders WHERE reminder_date = ? AND user_id = ?',
                              (date, user_id)) as cursor:
            reminders = []
            async for row in cursor:
                reminders.append(get_reminder_dict(row))
            return reminders


# Функция для поиска напоминаний по тегу
async def get_reminders_by_tag(tag, user_id):
    async with aiosqlite.connect(db_file) as db:
        async with db.execute('SELECT * FROM reminders WHERE tags LIKE ? AND user_id = ?',
                              ('%' + tag + '%', user_id)) as cursor:
            reminders = []
            async for row in cursor:
                reminders.append(get_reminder_dict(row))
            return reminders


# Функция для удаления напоминания по id
async def delete_reminder_by_id(reminder_id):
    async with aiosqlite.connect(db_file) as db:
        await db.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
        await db.commit()


# Функция для обновления текста напоминания по id
async def update_reminder_text_content(reminder_id, new_text_content):
    async with aiosqlite.connect(db_file) as db:
        await db.execute('''
            UPDATE reminders
            SET text_content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (new_text_content, reminder_id))
        await db.commit()


async def update_reminder_tags_content(reminder_id, new_tags):
    async with aiosqlite.connect(db_file) as db:
        await db.execute('''
            UPDATE reminders
            SET tags = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (new_tags, reminder_id))
        await db.commit()
