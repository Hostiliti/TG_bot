import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from Commands.handlers import StepsForm, get_start, get_help, show_today_tasks, send_remind_interval, add_time, add_time_answer, add_time_flag
from Data.DB import DataBase
from Loging.Logs import logs

DB = DataBase()
SF = StepsForm()

async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TG_API'))
    DB.db_connect()

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(send_remind_interval, trigger='interval', minutes=10, kwargs={'bot': bot})
    scheduler.start()
    
    dp = Dispatcher()
    dp.message.register(get_start, Command(commands=['start']))
    dp.message.register(get_help, lambda message: message.text == 'Help')
    dp.message.register(add_time, lambda message: message.text == 'Add time')
    dp.message.register(show_today_tasks, lambda message: message.text == 'Show today tasks')
    dp.message.register(add_time_answer, SF.GET_ANSWER)
    dp.message.register(add_time_flag, SF.GET_FLAG)

    try:
        logs().success('Бот запущен')
        await dp.start_polling(bot)
    finally:
        logs().success('Бот офф')
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())