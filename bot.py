import asyncio
import datetime
from os import getenv
from loguru import logger

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


def extract_additional_tokens(text):
    prompt = """
        If the user indicated something similar to a date in the message,
        then output it in JSON format, store it into "date_user" field,
        otherwise output empty JSON
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    logger.info(f"Start conversation with {message.from_user.id}")
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
    logger.info(f"Message from {user}")
    with Session() as session:
        context = get_context(session, user)
    context.append({"role": "user", "content": message.text})

    # TODO: log it
    tokens = extract_additional_tokens(message.text)
    print(f"Additional tokens: {tokens}")

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


# TODO: Use better aio loops or smt
if __name__ == "__main__":
    asyncio.run(main())
