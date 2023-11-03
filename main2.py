import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from Commands.func_comand import get_start, get_help, show_all_task, send_remind_cron, add_time_user
from Loging.Logs import logs

async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TG_API'))
    dp = Dispatcher()

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(send_remind_cron, trigger='cron', hour=0, minute=10, kwargs={'bot': bot})
    scheduler.start()

    dp.message.register(get_start, Command(commands=['start']))
    dp.message.register(get_help, lambda message: message.text == "Help")
    dp.message.register(show_all_task, lambda message: message.text == "Show all tasks")
    dp.message.register(add_time_user, lambda message: message.text == "Add Time tasks")

    try:
        logs().success('Бот запущен')
        await dp.start_polling(bot)
    finally:
        logs().success('Бот офф')
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())