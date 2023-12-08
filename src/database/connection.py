from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import (
    POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD,
    POSTGRES_HOST, POSTGRES_PORT
)


DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"  # noqa

engine = create_engine(DATABASE_URL)

Session = sessionmaker(
    expire_on_commit=False,
    bind=engine,
)

Base = declarative_base()
