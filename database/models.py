from sqlalchemy import Column, ForeignKey, String, BigInteger, DateTime, Integer

from database.connection import Base, engine
import asyncio


class Users(Base):
    __tablename__ = "users"

    telegram_id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    registation_date = Column(DateTime, nullable=True)


class ChatMessages(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey(
        Users.telegram_id), nullable=True, index=True)
    user_message = Column(String, nullable=True)
    user_message_datetime = Column(DateTime, nullable=True)
    openai_message = Column(String, nullable=True)
    openai_message_datetime = Column(DateTime, nullable=True)
    openai_response_duration_ms = Column(Integer, nullable=True)


Base.metadata.create_all(engine)
