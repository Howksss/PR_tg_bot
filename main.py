import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from functions import main_tab

load_dotenv()
async def main():
    load_dotenv()
    bot = Bot(os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_routers(main_tab.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
