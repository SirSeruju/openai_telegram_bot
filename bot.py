import asyncio
import datetime
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from openai import OpenAI

from database.connection import Session
from context import User, ChatMessage, get_context, update_context

client = OpenAI(api_key=getenv("OPENAI_API_KEY").strip())
TOKEN = getenv("TELEGRAM_TOKEN").strip()

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Hello, {hbold(message.from_user.full_name)}! Now we can talk!"
    )


@dp.message()
async def message_handler(message: types.Message) -> None:
    user = User(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        registation_date=datetime.datetime.now(),
    )
    with Session() as session:
        context = get_context(session, user)
    context.append({"role": "user", "content": message.text})

    # TODO: Как-то получать задержку напрямую
    start_response_timestamp = datetime.datetime.now().timestamp()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=context
    )
    response_delay = int((response.created - start_response_timestamp) * 1000)
    response_text = response.choices[0].message.content
    responce_message = await message.answer(response_text)

    context_upd = ChatMessage(
        user_message=message.text,
        user_message_datetime=message.date,
        openai_message=response_text,
        openai_message_datetime=responce_message.date,
        openai_response_delay_ms=response_delay,
    )
    with Session() as session:
        update_context(session, user, context_upd)


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
