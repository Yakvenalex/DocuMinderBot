import aiosqlite
from create_bot import db_file


async def add_note(user_id, note_type, text_content, file_id, tags):
    async with aiosqlite.connect(db_file) as db:
        await db.execute('''
            INSERT INTO notes (user_id, type, text_content, file_id, tags)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, note_type, text_content, file_id, tags))
        await db.commit()


def get_note_dict(row):
    return {'id': row[0], 'user_id': row[1], 'type': row[2], 'text_content': row[3],
            'file_id': row[4], 'tags': row[5], 'created_at': row[6], 'updated_at': row[7]
            }


# Функция для получения всех заметок пользователя
async def get_all_notes_by_user(user_id):
    async with aiosqlite.connect(db_file) as db:
        async with db.execute('SELECT * FROM notes WHERE user_id = ?', (user_id,)) as cursor:
            notes = []
            async for row in cursor:
                notes.append(get_note_dict(row))
            return notes


# Функция для поиска заметок по дате добавления
async def get_notes_by_date(user_id, date):
    async with aiosqlite.connect(db_file) as db:
        async with db.execute('SELECT * FROM notes WHERE user_id = ? AND DATE(created_at) = ?',
                              (user_id, date)) as cursor:
            notes = []
            async for row in cursor:
                notes.append(get_note_dict(row))
            return notes


# Функция для поиска заметок по тегу
async def get_notes_by_tag(user_id, tag):
    async with aiosqlite.connect(db_file) as db:
        async with db.execute('SELECT * FROM notes WHERE user_id = ? AND tags LIKE ?',
                              (user_id, '%' + tag + '%')) as cursor:
            notes = []
            async for row in cursor:
                notes.append(get_note_dict(row))
            return notes


# Функция для удаления заметки по id
async def delete_note_by_id(note_id):
    async with aiosqlite.connect(db_file) as db:
        await db.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        await db.commit()


# Функция для обновления текста заметки по id
async def update_note_text_content(note_id, new_text_content):
    async with aiosqlite.connect(db_file) as db:
        await db.execute('''
            UPDATE notes
            SET text_content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (new_text_content, note_id))
        await db.commit()


async def update_note_tags(note_id, new_tags):
    async with aiosqlite.connect(db_file) as db:
        await db.execute('''
            UPDATE notes
            SET tags = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (new_tags, note_id))
        await db.commit()
