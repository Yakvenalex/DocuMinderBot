import aiosqlite

from create_bot import db_file


async def create_tables():
    async with aiosqlite.connect(db_file) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT,
                text_content TEXT,
                file_id TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text_content TEXT,
                reminder_date DATE,
                reminder_time TIME,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        await db.commit()


# Функция для получения всех тегов пользователя в список
async def get_user_tags(user_id, table_name: str = 'notes'):
    if table_name == 'notes' or table_name == 'reminders':
        async with aiosqlite.connect(db_file) as db:
            async with db.execute(f'SELECT tags FROM {table_name} WHERE user_id = ?', (user_id,)) as cursor:
                tag_set = set()
                async for row in cursor:
                    tags_str = row[0]
                    if tags_str:
                        tags = tags_str.split(',')
                        tag_set.update(tag.strip().lower() for tag in tags)
                return list(tag_set)

