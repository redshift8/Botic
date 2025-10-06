import asyncio
from db import engine, metadata

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

if __name__ == '__main__':
    asyncio.run(create_tables())
