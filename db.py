import os
import datetime
from dotenv import load_dotenv
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL') or 'sqlite+aiosqlite:///./botic.db'

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

metadata = MetaData()

profiles = Table(
    'profiles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('chat_id', Integer, nullable=False),
    Column('gender', String, nullable=True),
    Column('age', Integer, nullable=True),
    Column('weight', Integer, nullable=True),
    Column('height', Integer, nullable=True),
    Column('activity', String, nullable=True),
    Column('goal', String, nullable=True),
    Column('created_at', DateTime, default=datetime.datetime.utcnow),
)

