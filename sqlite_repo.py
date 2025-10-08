from sqlalchemy import text
from db import AsyncSession
from abstract_repo import AbstractProfileRepo

class SQLiteProfileRepo(AbstractProfileRepo):
    def __init__(self, session_factory= AsyncSession):
        self._session_factory = session_factory

    async def save_profile(self, chat_id: int, data: dict) -> int:
        query = text("""
            INSERT INTO profiles (chat_id, gender, age, weight, height, activity, goal, target_weight)
            VALUES (:chat_id, :gender, :age, :weight, :height, :activity, :goal, :target_weight)
            """)

        params={
            'chat_id': chat_id,
            'gender':data.get('gender'),
            'age':data.get('age'),
            'weight':data.get('weight'),
            'height':data.get('height'),
            'activity':data.get('activity'),
            'target_weight': data.get('target_weight'),
            'goal':data.get('goal')
        }

        async with self._session_factory() as session:
            async with session.begin():
                await session.execute(query, params)
                last = await session.execute(text("SELECT last_insert_rowid()"))
                return int(last.scalar_one_or_none() or 0)