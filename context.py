from sqlalchemy.orm import Session

from database.models import Users, ChatMessages
import datetime
from sqlalchemy import select, desc
from sqlalchemy.dialects.postgresql import insert

from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    telegram_id: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    registation_date: datetime.datetime


class ChatMessage(BaseModel):
    user_message: str
    user_message_datetime: datetime.datetime
    openai_message: str
    openai_message_datetime: datetime.datetime
    openai_response_delay_ms: int


def get_context(session: Session, user: User, limit=100):
    """
    Получает данные о контексте из БД с ограничением на количество :limit:
    """
    query = select(ChatMessages).where(
        ChatMessages.user_id == user.telegram_id
    ).order_by(desc(ChatMessages.id)).limit(limit)
    messages = session.execute(query).all()
    context = []
    for message in messages:
        message = message[0]
        context += [
            {"role": "user", "content": message.user_message},
            {"role": "assistant", "content": message.openai_message}
        ]
    return context


def update_context(session: Session, user: User, message: ChatMessage):
    """
    Добавляет данные в контекст и вставляет/обновляет данные о пользователе
    """
    on_update_set = dict(user)
    on_update_set.pop("registation_date")
    query = insert(Users).values(
        telegram_id=user.telegram_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        registation_date=user.registation_date,
    ).on_conflict_do_update(
        index_elements=["telegram_id"],
        set_=on_update_set
    )
    session.execute(query)

    query = insert(ChatMessages).values(
        user_id=user.telegram_id,
        user_message=message.user_message,
        user_message_datetime=message.user_message_datetime,
        openai_message=message.openai_message,
        openai_message_datetime=message.openai_message_datetime,
        openai_response_delay_ms=message.openai_response_delay_ms,
    )
    session.execute(query)
    session.commit()
