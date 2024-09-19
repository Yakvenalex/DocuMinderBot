from sqlalchemy import select
from .database import async_session, engine, Base
from .models import Tag


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapper


async def get_or_create_tags(session, tag_texts: list[str], tag_group: str) -> list[Tag]:
    """Получает существующие теги или создает новые при необходимости."""
    # Получаем существующие теги
    existing_tags = await session.scalars(select(Tag).filter(Tag.tag_text.in_(tag_texts))).all()

    # Создаем недостающие теги
    existing_tag_texts = {tag.tag_text for tag in existing_tags}
    new_tags = [Tag(tag_text=tag_text, tag_group=tag_group) for tag_text in tag_texts if
                tag_text not in existing_tag_texts]

    if new_tags:
        session.add_all(new_tags)
        await session.flush()  # Сохраняем новые теги в сессии, но не коммитим

    return existing_tags + new_tags


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
