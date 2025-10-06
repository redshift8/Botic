import asyncio
from db import AsyncSession
from sqlalchemy import text

async def show_all_profiles():
    async with AsyncSession() as session:
        result = await session.execute(text("SELECT * FROM profiles"))
        rows = result.fetchall()
        for row in rows:
            print(dict(row._mapping)) 

asyncio.run(show_all_profiles())
