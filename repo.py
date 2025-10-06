from sqlalchemy import text
from db import AsyncSession


class ProfileRepo:
    def __init__(self, session_factory=AsyncSession):
        self._session_factory = session_factory

    async def save_profile(self, chat_id: int, data: dict) -> int:
        query = text("""
            INSERT INTO profiles (chat_id, gender, age, weight, height, activity, goal)
            VALUES (:chat_id, :gender, :age, :weight, :height, :activity, :goal)
            RETURNING id
        """)

        params = {
            'chat_id': chat_id,
            'gender': data.get('gender'),
            'age': data.get('age'),
            'weight': data.get('weight'),
            'height': data.get('height'),
            'activity': data.get('activity'),
            'goal': data.get('goal'),
        }

        async with self._session_factory() as session:
            async with session.begin():
                try:
                    res = await session.execute(query, params)
                    new_id = res.scalar_one_or_none()
                    return int(new_id) if new_id is not None else 0
                except Exception:
                    fallback = text("""
                        INSERT INTO profiles (chat_id, gender, age, weight, height, activity, goal)
                        VALUES (:chat_id, :gender, :age, :weight, :height, :activity, :goal)
                    """)
                    await session.execute(fallback, params)
                    try:
                        last = await session.execute(text('SELECT last_insert_rowid()'))
                        last_id = last.scalar_one_or_none()
                        return int(last_id) if last_id is not None else 0
                    except Exception:
                        return 0
