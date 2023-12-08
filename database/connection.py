from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv

POSTGRES_DB = getenv("POSTGRES_DB").strip()
POSTGRES_USER = getenv("POSTGRES_USER").strip()
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD").strip()
POSTGRES_HOST = getenv("POSTGRES_HOST").strip()
POSTGRES_PORT = getenv("POSTGRES_PORT").strip()
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"  # noqa

engine = create_engine(DATABASE_URL)

Session = sessionmaker(
    expire_on_commit=False,
    bind=engine,
)

Base = declarative_base()
