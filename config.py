from os import getenv

# TODO: Нормальная обработка ошибок

POSTGRES_DB = getenv("POSTGRES_DB").strip()
POSTGRES_USER = getenv("POSTGRES_USER").strip()
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD").strip()
POSTGRES_HOST = getenv("POSTGRES_HOST").strip()
POSTGRES_PORT = getenv("POSTGRES_PORT").strip()
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN").strip()
OPENAI_API_KEY = getenv("OPENAI_API_KEY").strip()
