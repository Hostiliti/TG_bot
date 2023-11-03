import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from Commands.handlers import get_start, get_help, show_today_tasks, send_remind_cron_breakfast, send_remind_cron_lunch, send_remind_cron_dinner
from Loging.Logs import logs

async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TG_API'))

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(send_remind_cron_breakfast, trigger='cron', hour=7, kwargs={'bot': bot})
    scheduler.add_job(send_remind_cron_lunch, trigger='cron', hour=13, kwargs={'bot': bot})
    scheduler.add_job(send_remind_cron_dinner, trigger='cron', hour=18, minute=8, kwargs={'bot': bot})
    scheduler.start()
    
    dp = Dispatcher()
    dp.message.register(get_start, Command(commands=['start']))
    dp.message.register(get_help, lambda message: message.text == 'Help')
    dp.message.register(show_today_tasks, lambda message: message.text == 'Show today tasks')

    try:
        logs().success('Бот запущен')
        await dp.start_polling(bot)
    finally:
        logs().success('Бот офф')
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())