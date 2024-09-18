import aiosqlite
from create_bot import db_file


async def register_user(user_id, username, full_name):
    async with aiosqlite.connect(db_file) as db:
        await db.execute('''
            INSERT INTO users (id, username, full_name)
            VALUES (?, ?, ?)
        ''', (user_id, username, full_name))
        await db.commit()


async def get_user(user_id):
    async with aiosqlite.connect(db_file) as db:
        async with db.execute('SELECT * FROM users WHERE id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'username': row[1],
                    'full_name': row[2],
                    'registered_at': row[3]
                }
            return None


# Метод для получения всех пользователей
async def get_all_users():
    async with aiosqlite.connect(db_file) as db:
        async with db.execute('SELECT * FROM users') as cursor:
            users = []
            async for row in cursor:
                users.append({
                    'id': row[0],
                    'username': row[1],
                    'full_name': row[2],
                    'registered_at': row[3]
                })
            return users
