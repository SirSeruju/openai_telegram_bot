import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from openai import OpenAI
client = OpenAI(api_key=getenv("OPENAI_API_KEY").strip())

conversation_history = []

TOKEN = getenv("TELEGRAM_TOKEN").strip()

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}! Now we can talk!")


@dp.message()
async def message_handler(message: types.Message) -> None:
    conversation_history.append({"role": "user", "content": message.text})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )
    response_text = response.choices[0].message.content
    await message.answer(response_text)
    conversation_history.append(
        {"role": "assistant", "content": response_text})
    for m in conversation_history:
        print(m)


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
