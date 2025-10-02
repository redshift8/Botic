
import asyncio
from aiogram import Bot, Dispatcher
from handlers import router
import logging
from dotenv import load_dotenv
import os


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


logging.basicConfig(level=logging.INFO) 
   

if __name__ == "__main__":
    asyncio.run(main())
