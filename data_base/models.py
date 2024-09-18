from datetime import date, time

from sqlalchemy import BigInteger, Integer, Text, Date, Time, ForeignKey, String, Table, Column, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base

# Промежуточная таблица для связи заметок с тегами
note_tag_association = Table(
    'note_tag_association', Base.metadata,
    Column('note_id', ForeignKey('notes.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.tag_id'), primary_key=True)
)

# Промежуточная таблица для связи напоминаний с тегами
reminder_tag_association = Table(
    'reminder_tag_association', Base.metadata,
    Column('reminder_id', ForeignKey('reminders.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.tag_id'), primary_key=True)
)


# Модель для таблицы пользователей
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)

    # Связи с заметками и напоминаниями
    notes: Mapped[list["Note"]] = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    reminders: Mapped[list["Reminder"]] = relationship("Reminder", back_populates="user", cascade="all, delete-orphan")


# Модель для таблицы заметок
class Note(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=True)
    content_text: Mapped[str] = mapped_column(Text, nullable=True)
    file_id: Mapped[str] = mapped_column(String, nullable=True)

    # Связь с пользователями и тегами
    user: Mapped["User"] = relationship("User", back_populates="notes")
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary=note_tag_association, back_populates="notes")


# Модель для таблицы напоминаний
class Reminder(Base):
    __tablename__ = 'reminders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    content_text: Mapped[str] = mapped_column(Text, nullable=True)
    reminder_date: Mapped[date] = mapped_column(Date, nullable=False)
    reminder_time: Mapped[time] = mapped_column(Time, nullable=False)

    # Связь с пользователями и тегами
    user: Mapped["User"] = relationship("User", back_populates="reminders")
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary=reminder_tag_association, back_populates="reminders")


# Модель для таблицы тегов
class Tag(Base):
    __tablename__ = 'tags'

    tag_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tag_group: Mapped[str] = mapped_column(Enum('notes', 'reminders', name='tag_group_enum'), nullable=False)
    tag_text: Mapped[str] = mapped_column(String, nullable=False)

    # Связь с заметками и напоминаниями
    notes: Mapped[list["Note"]] = relationship("Note", secondary=note_tag_association, back_populates="tags")
    reminders: Mapped[list["Reminder"]] = relationship("Reminder", secondary=reminder_tag_association,
                                                       back_populates="tags")
