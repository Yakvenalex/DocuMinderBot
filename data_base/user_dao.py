from sqlalchemy import select
from create_bot import logger
from .base import connection
from .models import User


@connection
async def set_user(session, tg_id: int, username: str, full_name: str):
    user = await session.scalar(select(User).filter_by(id=tg_id))

    if not user:
        session.add(User(id=tg_id, username=username, full_name=full_name))
        await session.commit()
        logger.info(f"Зарегистрировал пользователя с ID {tg_id}!")
        return None
    else:
        logger.info(f"Пользователь с ID {tg_id} найден!")
        return user
